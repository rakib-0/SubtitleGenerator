import os
import logging
from rich.logging import RichHandler
from rich.console import Console

console = Console()

def setup_logging():
    """Set up logging configuration with Rich handler."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)]
    )
    return logging.getLogger("subtitle_generator")

def validate_input(args):
    """Validate command line arguments.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        bool: True if validation passes, False otherwise
    """
    logger = logging.getLogger("subtitle_generator")
    
    # Check if either input file or directory is provided
    if not args.input and not args.input_dir:
        console.print("❌ [red]Error: Either --input or --input_dir must be provided[/red]")
        return False
    
    # Check if both input file and directory are provided
    if args.input and args.input_dir:
        console.print("❌ [red]Error: Cannot specify both --input and --input_dir[/red]")
        return False
    
    # Check if output is provided for single file
    if args.input and not args.output:
        console.print("❌ [red]Error: --output must be provided when using --input[/red]")
        return False
    
    # Check if output directory is provided for batch processing
    if args.input_dir and not args.output_dir:
        console.print("❌ [red]Error: --output_dir must be provided when using --input_dir[/red]")
        return False
    
    # Validate input file existence
    if args.input and not os.path.isfile(args.input):
        console.print(f"❌ [red]Error: Input file does not exist: {args.input}[/red]")
        return False
    
    # Validate input directory existence
    if args.input_dir and not os.path.isdir(args.input_dir):
        console.print(f"❌ [red]Error: Input directory does not exist: {args.input_dir}[/red]")
        return False
    
    # All validations passed
    console.print("✅ [green]Input validation successful![/green]")
    return True

def create_output_dir(directory):
    """Create output directory if it doesn't exist.
    
    Args:
        directory (str): Directory path to create
    """
    if directory:
        try:
            os.makedirs(directory, exist_ok=True)
            console.print(f"📁 [green]Created output directory: {directory}[/green]")
        except Exception as e:
            console.print(f"❌ [red]Error creating output directory: {str(e)}[/red]") 