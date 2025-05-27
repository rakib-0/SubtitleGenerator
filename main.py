#!/usr/bin/env python3

import argparse
import os
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from src.transcriber import WhisperTranscriber
from src.translator import Translator
from src.formatter import SubtitleFormatter
from src.utils import setup_logging, validate_input, create_output_dir

console = Console()

def parse_arguments():
    parser = argparse.ArgumentParser(
        description='🎬 Interactive Video Subtitle Generator 🎥',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--input', type=str, help='📁 Input video file path')
    parser.add_argument('--input_dir', type=str, help='📂 Input directory containing video files')
    parser.add_argument('--output', type=str, help='📝 Output subtitle file path')
    parser.add_argument('--output_dir', type=str, help='📂 Output directory for subtitle files')
    parser.add_argument('--language', type=str, default='en', help='🌐 Target language code (e.g., en, es, fr, fa)')
    parser.add_argument('--model', type=str, default='base', 
                      choices=['tiny', 'base', 'small', 'medium', 'large'],
                      help='🤖 Whisper model size')
    parser.add_argument('--format', type=str, default='srt',
                      choices=['srt', 'vtt'],
                      help='📄 Output subtitle format')
    parser.add_argument('--gpu', action='store_true', help='⚡ Use GPU acceleration if available')
    
    # Translation quality options
    parser.add_argument('--translation-quality', type=str, default='balanced',
                      choices=['fast', 'balanced', 'high'],
                      help='🎯 Translation quality mode (fast/balanced/high)')
    parser.add_argument('--chunk-size', type=int, default=3000,
                      help='📝 Maximum chunk size for translation (smaller = more accurate)')
    parser.add_argument('--context-aware', action='store_true', default=True,
                      help='🧠 Use context-aware translation for better accuracy')
    
    return parser.parse_args()

def create_progress():
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=console
    )

def process_single_video(input_path, output_path, args, transcriber, translator, formatter):
    """Process a single video file."""
    try:
        with create_progress() as progress:
            # Transcription
            task1 = progress.add_task("🎙️ [cyan]Transcribing audio...", total=100)
            transcription = transcriber.transcribe(input_path, progress, task1)
            
            console.print(f"\n📝 [cyan]Detected language: {transcription['language']}[/cyan]")
            console.print(f"🎯 [cyan]Target language: {args.language}[/cyan]")
            console.print(f"⚙️ [cyan]Translation quality: {args.translation_quality}[/cyan]")
            
            # Translation (if needed)
            task2 = progress.add_task("🌍 [yellow]Translating...", total=100)
            if transcription['language'] != args.language:
                console.print(f"\n🔄 [cyan]Translating from {transcription['language']} to {args.language}[/cyan]")
                
                # Configure translator based on quality settings
                translator.configure_quality(
                    quality_mode=args.translation_quality,
                    chunk_size=args.chunk_size,
                    context_aware=args.context_aware
                )
                
                translated_text = translator.translate(
                    text=transcription['text'],
                    source_lang=transcription['language'],
                    target_lang=args.language,
                    progress=progress,
                    task_id=task2
                )
                
                # Update segments with translated text
                segments = transcription['segments']
                if len(segments) > 0:
                    # Split translated text into roughly equal parts based on original segment lengths
                    total_chars = len(translated_text)
                    total_orig_chars = len(transcription['text'])
                    char_ratio = total_chars / total_orig_chars if total_orig_chars > 0 else 1
                    
                    start_idx = 0
                    for segment in segments:
                        orig_len = len(segment['text'])
                        target_len = int(orig_len * char_ratio)
                        # Find the nearest sentence end or space
                        end_idx = min(start_idx + target_len, len(translated_text))
                        while end_idx < len(translated_text) and translated_text[end_idx] not in '.!?。，':
                            end_idx += 1
                        segment['text'] = translated_text[start_idx:end_idx].strip()
                        start_idx = end_idx
            else:
                console.print("\n✨ [green]No translation needed (same language)[/green]")
                progress.update(task2, advance=100)
                segments = transcription['segments']
            
            # Formatting
            task3 = progress.add_task("📝 [green]Formatting subtitles...", total=100)
            formatter.format_subtitles(
                text=translated_text if 'translated_text' in locals() else transcription['text'],
                segments=segments,
                output_path=output_path,
                format=args.format,
                progress=progress,
                task_id=task3
            )
            
        console.print(f"✨ [green]Successfully generated subtitles: {output_path}")
        return True
    except Exception as e:
        console.print(f"❌ [red]Error processing {input_path}: {str(e)}")
        return False

def main():
    console.print("\n🎬 [bold cyan]Interactive Video Subtitle Generator[/bold cyan] 🎥")
    console.print("✨ [italic]Enhanced with Multi-Engine Translation for Superior Accuracy[/italic] ✨\n")
    
    args = parse_arguments()
    logger = setup_logging()
    
    # Validate inputs and create output directory
    if not validate_input(args):
        return
    
    create_output_dir(args.output_dir if args.output_dir else os.path.dirname(args.output))
    
    # Initialize components with loading messages
    console.print("🤖 [cyan]Loading Whisper model...[/cyan]")
    transcriber = WhisperTranscriber(model_name=args.model, use_gpu=args.gpu)
    
    console.print("🌐 [yellow]Initializing enhanced translator...[/yellow]")
    translator = Translator()
    
    console.print("📝 [green]Setting up subtitle formatter...[/green]\n")
    formatter = SubtitleFormatter()
    
    if args.input_dir:
        # Batch processing
        success_count = 0
        total_files = 0
        
        console.print("📂 [bold]Starting batch processing...[/bold]\n")
        
        for root, _, files in os.walk(args.input_dir):
            for file in files:
                if file.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
                    total_files += 1
                    input_path = os.path.join(root, file)
                    rel_path = os.path.relpath(input_path, args.input_dir)
                    output_path = os.path.join(
                        args.output_dir,
                        os.path.splitext(rel_path)[0] + '.' + args.format
                    )
                    
                    console.print(f"\n🎥 [bold]Processing: {rel_path}")
                    if process_single_video(input_path, output_path, args, 
                                         transcriber, translator, formatter):
                        success_count += 1
        
        # Final summary with emojis
        console.print(f"\n📊 [bold]Batch processing summary:[/bold]")
        console.print(f"✅ Successfully processed: {success_count} files")
        console.print(f"❌ Failed: {total_files - success_count} files")
        console.print(f"📈 Success rate: {(success_count/total_files)*100:.1f}%\n")
    
    else:
        # Single file processing
        console.print("🎥 [bold]Processing single video...[/bold]\n")
        process_single_video(args.input, args.output, args, transcriber, translator, formatter)
    
    console.print("✨ [bold green]All done! Thank you for using the Interactive Video Subtitle Generator![/bold green] 🎉\n")

if __name__ == '__main__':
    main() 