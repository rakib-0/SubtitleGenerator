import whisper
import torch
import numpy as np
from pydub import AudioSegment
import tempfile
import os
import subprocess
from rich.console import Console

console = Console()

def get_ffmpeg_path():
    """Get the FFmpeg path."""
    try:
        # Try using which command on Unix-like systems
        ffmpeg_path = subprocess.check_output(['which', 'ffmpeg']).decode().strip()
        return ffmpeg_path
    except:
        # Check common installation paths
        common_paths = [
            '/usr/bin/ffmpeg',
            '/usr/local/bin/ffmpeg',
            '/opt/homebrew/bin/ffmpeg',  # Common Homebrew path on M1 Macs
            '/usr/local/Cellar/ffmpeg',  # Homebrew Cellar path
        ]
        for path in common_paths:
            if os.path.exists(path):
                return path
        return 'ffmpeg'  # Default to just the command name

class WhisperTranscriber:
    def __init__(self, model_name='base', use_gpu=False):
        """Initialize the Whisper transcriber.
        
        Args:
            model_name (str): Name of the Whisper model to use
            use_gpu (bool): Whether to use GPU acceleration
        """
        # Set FFmpeg path for pydub
        AudioSegment.converter = get_ffmpeg_path()
        
        self.device = "cuda" if use_gpu and torch.cuda.is_available() else "cpu"
        if use_gpu and torch.cuda.is_available():
            console.print("⚡ [green]GPU acceleration enabled![/green]")
        else:
            console.print("💻 [yellow]Running on CPU[/yellow]")
        
        console.print(f"🔄 [cyan]Loading {model_name} model...[/cyan]")
        try:
            # Clear any cached models to avoid conflicts
            torch.cuda.empty_cache() if torch.cuda.is_available() else None
            
            # Load model with error handling
            self.model = whisper.load_model(model_name, device=self.device)
            
            # Verify model is working by testing with a small dummy input
            self._test_model()
            
            console.print("✅ [green]Model loaded and verified successfully![/green]")
        except Exception as e:
            console.print(f"❌ [red]Error loading {model_name} model: {str(e)}[/red]")
            console.print("🔄 [yellow]Trying to load 'base' model as fallback...[/yellow]")
            try:
                # Fallback to base model
                self.model = whisper.load_model('base', device=self.device)
                self._test_model()
                console.print("✅ [green]Fallback model loaded successfully![/green]")
            except Exception as fallback_error:
                console.print(f"❌ [red]Fallback model also failed: {str(fallback_error)}[/red]")
                raise Exception(f"Failed to load any Whisper model: {str(e)}")
    
    def _test_model(self):
        """Test the model with a small dummy input to ensure it's working."""
        try:
            # Create a small dummy audio (1 second of silence)
            dummy_audio = np.zeros(16000, dtype=np.float32)  # 1 second at 16kHz
            
            # Test transcription
            result = self.model.transcribe(dummy_audio, language='en', task='transcribe')
            
            # If we get here, the model is working
            return True
        except Exception as e:
            raise Exception(f"Model test failed: {str(e)}")
    
    def _preprocess_audio(self, video_path):
        """Extract and preprocess audio from video file."""
        try:
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_audio:
                # Extract audio using pydub with specific parameters
                audio = AudioSegment.from_file(video_path)
                
                # Convert to mono and set sample rate to 16kHz (Whisper's expected format)
                audio = audio.set_channels(1)
                audio = audio.set_frame_rate(16000)
                
                # Export with specific parameters
                audio.export(
                    temp_audio.name, 
                    format='wav',
                    parameters=["-ac", "1", "-ar", "16000"]  # Mono, 16kHz
                )
                
                return temp_audio.name
        except Exception as e:
            console.print(f"❌ [red]Error preprocessing audio: {str(e)}[/red]")
            raise
    
    def transcribe(self, video_path, progress=None, task_id=None):
        """Transcribe audio from a video file.
        
        Args:
            video_path (str): Path to the video file
            progress (Progress, optional): Rich progress instance
            task_id: Task ID for progress tracking
            
        Returns:
            dict: Transcription results including text, segments, and detected language
        """
        audio_path = None
        try:
            # Update progress
            if progress and task_id:
                progress.update(task_id, advance=10, description="🎵 [cyan]Extracting audio...")
            
            # Preprocess audio
            audio_path = self._preprocess_audio(video_path)
            
            if progress and task_id:
                progress.update(task_id, advance=20, description="📊 [cyan]Processing audio waveform...")
            
            # Load audio using whisper's load_audio function with proper error handling
            try:
                audio = whisper.load_audio(audio_path)
            except Exception as e:
                console.print(f"⚠️ [yellow]Whisper load_audio failed, trying alternative method...[/yellow]")
                # Alternative: load audio manually
                from scipy.io import wavfile
                import librosa
                
                try:
                    # Try with librosa
                    audio, sr = librosa.load(audio_path, sr=16000, mono=True)
                    audio = audio.astype(np.float32)
                except:
                    # Try with scipy
                    sr, audio = wavfile.read(audio_path)
                    if sr != 16000:
                        import scipy.signal
                        audio = scipy.signal.resample(audio, int(len(audio) * 16000 / sr))
                    audio = audio.astype(np.float32) / 32768.0  # Normalize
            
            if progress and task_id:
                progress.update(task_id, advance=20, description="🔍 [cyan]Detecting language...")
            
            # Detect language with error handling
            try:
                audio_segment = whisper.pad_or_trim(audio)
                mel = whisper.log_mel_spectrogram(audio_segment).to(self.device)
                _, probs = self.model.detect_language(mel)
                detected_language = max(probs, key=probs.get)
            except Exception as e:
                console.print(f"⚠️ [yellow]Language detection failed, defaulting to English: {str(e)}[/yellow]")
                detected_language = 'en'
            
            if progress and task_id:
                progress.update(task_id, advance=20, description="🎙️ [cyan]Converting speech to text...")
            
            # Transcribe with enhanced error handling
            try:
                result = self.model.transcribe(
                    audio,
                    language=detected_language,
                    task="transcribe",
                    verbose=False,  # Reduce verbosity
                    fp16=False  # Disable FP16 to avoid precision issues
                )
            except Exception as e:
                console.print(f"⚠️ [yellow]Transcription with detected language failed, trying auto-detect...[/yellow]")
                # Retry without specifying language
                result = self.model.transcribe(
                    audio,
                    task="transcribe",
                    verbose=False,
                    fp16=False
                )
                detected_language = result.get('language', 'en')
            
            if progress and task_id:
                progress.update(task_id, advance=30, description="✨ [cyan]Finalizing transcription...")
            
            # Clean up temporary file
            if audio_path and os.path.exists(audio_path):
                os.unlink(audio_path)
            
            # Validate results
            if not result.get('text') or not result.get('segments'):
                raise Exception("Transcription returned empty results")
            
            console.print(f"✅ [green]Transcription completed! Language: {detected_language}[/green]")
            
            return {
                'text': result['text'],
                'segments': result['segments'],
                'language': detected_language
            }
            
        except Exception as e:
            if audio_path and os.path.exists(audio_path):
                os.unlink(audio_path)
            console.print(f"❌ [red]Transcription failed: {str(e)}[/red]")
            raise Exception(f"Transcription failed: {str(e)}") 