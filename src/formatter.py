import os
from datetime import timedelta

class SubtitleFormatter:
    def __init__(self):
        """Initialize the subtitle formatter."""
        pass
    
    def _format_timestamp(self, seconds, format='srt'):
        """Convert seconds to timestamp format.
        
        Args:
            seconds (float): Time in seconds
            format (str): Output format ('srt' or 'vtt')
            
        Returns:
            str: Formatted timestamp
        """
        td = timedelta(seconds=seconds)
        hours = td.seconds // 3600
        minutes = (td.seconds % 3600) // 60
        seconds = td.seconds % 60
        milliseconds = td.microseconds // 1000
        
        if format == 'vtt':
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
        else:  # srt
            return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"
    
    def _format_srt(self, segments):
        """Format subtitles in SRT format."""
        srt_content = []
        
        for i, segment in enumerate(segments, 1):
            start_time = self._format_timestamp(segment['start'])
            end_time = self._format_timestamp(segment['end'])
            text = segment['text'].strip()
            
            srt_content.extend([
                str(i),
                f"{start_time} --> {end_time}",
                text,
                ""
            ])
        
        return "\n".join(srt_content)
    
    def _format_vtt(self, segments):
        """Format subtitles in WebVTT format."""
        vtt_content = ["WEBVTT", ""]
        
        for i, segment in enumerate(segments, 1):
            start_time = self._format_timestamp(segment['start'], format='vtt')
            end_time = self._format_timestamp(segment['end'], format='vtt')
            text = segment['text'].strip()
            
            vtt_content.extend([
                f"{start_time} --> {end_time}",
                text,
                ""
            ])
        
        return "\n".join(vtt_content)
    
    def format_subtitles(self, text, segments, output_path, format='srt', progress=None, task_id=None):
        """Format and save subtitles to file.
        
        Args:
            text (str): Full transcribed text (unused, kept for API consistency)
            segments (list): List of segment dictionaries with timing information
            output_path (str): Path to save the subtitle file
            format (str): Output format ('srt' or 'vtt')
            progress (Progress, optional): Rich progress instance
            task_id: Task ID for progress tracking
        """
        try:
            if progress and task_id:
                progress.update(task_id, advance=30, description=f"[green]Formatting {format.upper()}...")
            
            # Create output directory if it doesn't exist
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Format content based on chosen format
            content = self._format_srt(segments) if format == 'srt' else self._format_vtt(segments)
            
            if progress and task_id:
                progress.update(task_id, advance=40, description="[green]Writing to file...")
            
            # Write to file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            if progress and task_id:
                progress.update(task_id, advance=30)
                
        except Exception as e:
            raise Exception(f"Subtitle formatting failed: {str(e)}") 