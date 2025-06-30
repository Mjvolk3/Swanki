
#!/usr/bin/env python3
"""Send existing cards to Anki from a directory.

This script looks for cards-with-audio.md or cards-plain.md in a directory,
creates the corresponding anki-cards file with deck header, and sends it to Anki.
"""
import argparse
import sys
from pathlib import Path
import logging
import os

# Add the swanki package directory to Python path
swanki_root = Path(__file__).parent.parent
if str(swanki_root) not in sys.path:
    sys.path.insert(0, str(swanki_root))

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


def prepare_anki_file(input_path: Path, deck_name: str) -> Path:
    """Prepare markdown file for Anki import by adding deck header.
    
    Parameters
    ----------
    input_path : Path
        Path to the original cards file
    deck_name : str
        Name of the Anki deck
        
    Returns
    -------
    Path
        Path to prepared Anki file
    """
    # Create anki- prefixed filename
    if input_path.name == "cards-with-audio.md":
        anki_filename = "anki-cards-with-audio.md"
    elif input_path.name == "cards-plain.md":
        anki_filename = "anki-cards.md"
    else:
        anki_filename = f"anki-{input_path.name}"
    
    anki_path = input_path.parent / anki_filename
    
    # Read original content
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Write with deck header
    with open(anki_path, 'w', encoding='utf-8') as f:
        f.write(f"# {deck_name}\n\n")
        f.write(content)
    
    logger.info(f"Created {anki_path}")
    return anki_path


def send_directory_to_anki(directory: Path, deck_name: str = None, host: str = '127.0.0.1', port: int = 8765):
    """Send cards from a directory to Anki.
    
    Looks for cards-with-audio.md or cards-plain.md, creates the anki- version,
    and sends to Anki using the modern AnkiProcessor.
    
    Parameters
    ----------
    directory : Path
        Directory containing card files
    deck_name : str, optional
        Deck name (defaults to directory name)
    host : str, optional
        AnkiConnect host
    port : int, optional
        AnkiConnect port
    """
    # Look for card files
    cards_with_audio = directory / "cards-with-audio.md"
    cards_plain = directory / "cards-plain.md"
    
    # Determine which file to use
    if cards_with_audio.exists():
        input_file = cards_with_audio
        logger.info(f"Found {cards_with_audio}")
    elif cards_plain.exists():
        input_file = cards_plain
        logger.info(f"Found {cards_plain}")
    else:
        logger.error(f"No cards file found in {directory}")
        logger.error("Expected: cards-with-audio.md or cards-plain.md")
        return False
    
    # Use directory name as deck name if not provided
    if deck_name is None:
        deck_name = directory.name
        # Remove numbering suffix if present (e.g., "luoWhenCausalInference2020_23" -> "luoWhenCausalInference2020")
        if "_" in deck_name and deck_name.split("_")[-1].isdigit():
            deck_name = "_".join(deck_name.split("_")[:-1])
    
    # Prepare anki file
    anki_file = prepare_anki_file(input_file, deck_name)
    
    # Import AnkiProcessor
    try:
        from ..processing.anki_processor import AnkiProcessor
    except ImportError:
        # Fallback import for script usage
        import sys
        sys.path.insert(0, str(swanki_root))
        from swanki.processing.anki_processor import AnkiProcessor
    
    # Send to Anki using modern processor
    try:
        anki_processor = AnkiProcessor(host, port)
        cards_added, cards_updated = anki_processor.send_cards_from_file(
            file_path=anki_file,
            deck_name=deck_name,
            update_existing=True,
            upload_media=True,
            sync_after=False
        )
        
        logger.info(f"✓ Successfully sent to Anki deck '{deck_name}': {cards_added} added, {cards_updated} updated")
        return True
        
    except Exception as e:
        logger.error(f"✗ Failed to send cards to Anki: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Send existing cards to Anki from directories",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Send from single directory (uses directory name as deck)
  swanki-to-anki /path/to/card/directory
  
  # Send with custom deck name
  swanki-to-anki /path/to/card/directory --deck "My Custom Deck"
  
  # Send from multiple directories
  swanki-to-anki /path/to/dir1 /path/to/dir2 /path/to/dir3
  
  # Send with custom AnkiConnect settings
  swanki-to-anki /path/to/directory --host 192.168.1.100 --port 8765
        """
    )
    
    parser.add_argument(
        'directories',
        nargs='+',
        type=Path,
        help='Directory/directories containing cards-with-audio.md or cards-plain.md'
    )
    
    parser.add_argument(
        '--deck',
        type=str,
        help='Deck name (defaults to directory name)'
    )
    
    parser.add_argument(
        '--host',
        type=str,
        default='127.0.0.1',
        help='AnkiConnect host (default: 127.0.0.1)'
    )
    
    parser.add_argument(
        '--port',
        type=int,
        default=8765,
        help='AnkiConnect port (default: 8765)'
    )
    
    args = parser.parse_args()
    
    # Process each directory
    success_count = 0
    for directory in args.directories:
        if not directory.is_dir():
            logger.error(f"Not a directory: {directory}")
            continue
        
        logger.info(f"\nProcessing: {directory}")
        if send_directory_to_anki(directory, args.deck, args.host, args.port):
            success_count += 1
        logger.info("-" * 50)
    
    # Summary
    total = len(args.directories)
    if success_count == total:
        logger.info(f"\n✓ All {total} directories processed successfully!")
    else:
        logger.info(f"\n⚠ Processed {success_count}/{total} directories successfully")
        sys.exit(1)


if __name__ == "__main__":
    main()