"""Modern Anki integration processor for Swanki.

This module provides AnkiConnect integration for sending cards to Anki,
replacing the legacy md_to_anki.py functionality with a cleaner API.
Supports creating decks, adding/updating cards, and uploading media files.

Classes
-------
AnkiProcessor
    Process and send cards to Anki using AnkiConnect

Examples
--------
>>> from swanki.processing import AnkiProcessor
>>> from pathlib import Path
>>> 
>>> processor = AnkiProcessor(host="127.0.0.1", port=8765)
>>> if processor.check_connection():
...     cards_added, cards_updated = processor.send_cards_from_file(
...         file_path=Path("cards.md"),
...         deck_name="My::Deck",
...         update_existing=True
...     )
...     print(f"Added: {cards_added}, Updated: {cards_updated}")

Notes
-----
Requires Anki to be running with the AnkiConnect addon installed.
See https://ankiweb.net/shared/info/2055492159 for installation.
"""

import base64
import json
import logging
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple, Optional

import requests

logger = logging.getLogger(__name__)

# Regex patterns
TAG_LINE_RE = re.compile(r"^\s*[-*]\s*(#.+)$")
TAG_SPLIT_RE = re.compile(r",\s*")
IMAGE_RE = re.compile(r"!\[.*?\]\((.*?)\)")
AUDIO_LINK_RE = re.compile(r"\[audio(?:-front|-back)?\]\((.*?)\)")
MATH_FENCE_RE = re.compile(r"```+\s*([$]{1,2}[\s\S]*?[$]{1,2})\s*```+", re.DOTALL)
HR_SPLIT_RE = re.compile(r"^[*-]{3,}\s*$")


class AnkiProcessor:
    """Process and send cards to Anki using AnkiConnect.
    
    Handles all Anki integration including deck creation, card addition
    and updates, media file uploads, and synchronization. Supports both
    Basic and Cloze card types with automatic detection.
    
    Parameters
    ----------
    host : str, optional
        AnkiConnect host address (default is "127.0.0.1")
    port : int, optional
        AnkiConnect port number (default is 8765)
    
    Attributes
    ----------
    host : str
        AnkiConnect host
    port : int
        AnkiConnect port
    url : str
        Full AnkiConnect URL
    
    Methods
    -------
    check_connection()
        Verify AnkiConnect is available
    send_cards_from_file(file_path, deck_name, ...)
        Send cards from markdown file to Anki
    
    Examples
    --------
    >>> processor = AnkiProcessor()
    >>> 
    >>> # Check connection
    >>> if not processor.check_connection():
    ...     print("Please start Anki with AnkiConnect")
    >>> 
    >>> # Send cards
    >>> added, updated = processor.send_cards_from_file(
    ...     Path("flashcards.md"),
    ...     "Biology::Cell Structure"
    ... )
    """
    
    def __init__(self, host: str = "127.0.0.1", port: int = 8765):
        """Initialize AnkiProcessor.
        
        Parameters
        ----------
        host : str, optional
            AnkiConnect host address (default is "127.0.0.1")
        port : int, optional
            AnkiConnect port number (default is 8765)
        """
        self.host = host
        self.port = port
        self.url = f"http://{host}:{port}"
        
    def check_connection(self) -> bool:
        """Check if AnkiConnect is available.
        
        Returns
        -------
        bool
            True if AnkiConnect is reachable, False otherwise
        
        Examples
        --------
        >>> processor = AnkiProcessor()
        >>> if processor.check_connection():
        ...     print("Anki is running")
        ... else:
        ...     print("Please start Anki")
        """
        try:
            response = requests.post(
                self.url,
                json={"action": "version", "version": 6}
            )
            return response.status_code == 200
        except Exception:
            return False
    
    def send_cards_from_file(
        self,
        file_path: Path,
        deck_name: str,
        update_existing: bool = True,
        upload_media: bool = True,
        sync_after: bool = False
    ) -> Tuple[int, int]:
        """Send cards from a markdown file to Anki.
        
        Parses a markdown file for flashcards and sends them to Anki.
        Automatically detects card types (Basic or Cloze) and handles
        media uploads.
        
        Parameters
        ----------
        file_path : Path
            Path to markdown file containing cards
        deck_name : str
            Target deck name (use :: for nested decks, e.g., "Parent::Child")
        update_existing : bool, optional
            Whether to update existing cards (default is True)
        upload_media : bool, optional
            Whether to upload referenced media files (default is True)
        sync_after : bool, optional
            Whether to sync Anki after sending (default is False)
        
        Returns
        -------
        Tuple[int, int]
            Number of cards (added, updated)
        
        Raises
        ------
        RuntimeError
            If AnkiConnect is not available
        
        Examples
        --------
        >>> processor = AnkiProcessor()
        >>> added, updated = processor.send_cards_from_file(
        ...     Path("biology_cards.md"),
        ...     "Science::Biology::Cells",
        ...     update_existing=True,
        ...     upload_media=True
        ... )
        >>> print(f"Sent {added} new cards, updated {updated} existing")
        
        Notes
        -----
        Card format in markdown:
        - Cards start with ## (H2 header)
        - Front/back separated by % or ---
        - Tags as #tag1, #tag2 or - #tag
        - Cloze cards detected by {{c1::text}} syntax
        """
        # Check connection
        if not self.check_connection():
            raise RuntimeError("Cannot connect to AnkiConnect. Is Anki running with AnkiConnect installed?")
        
        logger.info(f"Sending cards to Anki deck: {deck_name}")
        
        # Read and parse the markdown file
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [line.rstrip('\n') for line in f]
        
        # Extract cards
        cards = self._extract_cards(lines)
        logger.info(f"Found {len(cards)} cards to process")
        
        # Create deck
        self._create_deck(deck_name)
        
        # Upload media first if requested
        if upload_media:
            media_count = self._upload_media_files(file_path)
            logger.info(f"Uploaded {media_count} media files")
        
        # Process each card
        cards_added = 0
        cards_updated = 0
        
        for card in cards:
            # Determine card type
            is_cloze = "{{c" in card['front']
            model_name = "Cloze" if is_cloze else "Basic"
            
            # Prepare fields
            if is_cloze:
                fields = {
                    "Text": card['front'] + "\n" + card['back'],
                    "Extra": ""
                }
                search_key = "Text"
            else:
                fields = {
                    "Front": card['front'],
                    "Back": card['back']
                }
                search_key = "Front"
            
            # Check if card exists
            query = f'deck:"{deck_name}" {search_key}:"{fields[search_key]}"'
            existing_ids = self._find_notes(query)
            
            if not existing_ids:
                # Add new card
                note_id = self._add_note(deck_name, model_name, fields, card['tags'])
                if note_id:
                    cards_added += 1
                    logger.debug(f"Added new card: {card['front'][:50]}...")
            elif update_existing:
                # Update existing card
                note_info = self._get_note_info(existing_ids[:1])
                if note_info and self._fields_differ(note_info[0]['fields'], fields):
                    if self._update_note(existing_ids[0], fields):
                        cards_updated += 1
                        logger.debug(f"Updated card: {card['front'][:50]}...")
        
        # Sync if requested
        if sync_after:
            self._sync()
        
        logger.info(f"Successfully processed {len(cards)} cards: {cards_added} added, {cards_updated} updated")
        return cards_added, cards_updated
    
    def _create_deck(self, deck_name: str) -> bool:
        """Create a deck if it doesn't exist.
        
        Parameters
        ----------
        deck_name : str
            Name of deck to create (supports :: hierarchy)
        
        Returns
        -------
        bool
            True if successful, False otherwise
        """
        try:
            response = requests.post(
                self.url,
                json={
                    "action": "createDeck",
                    "version": 6,
                    "params": {"deck": deck_name}
                }
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Failed to create deck {deck_name}: {e}")
            return False
    
    def _add_note(self, deck_name: str, model_name: str, fields: Dict[str, str], tags: List[str]) -> Optional[int]:
        """Add a new note to Anki.
        
        Parameters
        ----------
        deck_name : str
            Target deck name
        model_name : str
            Note type ("Basic" or "Cloze")
        fields : Dict[str, str]
            Field values for the note
        tags : List[str]
            Tags to apply to the note
        
        Returns
        -------
        int or None
            Note ID if successful, None if failed
        """
        note = {
            "deckName": deck_name,
            "modelName": model_name,
            "fields": fields,
            "tags": tags
        }
        
        try:
            response = requests.post(
                self.url,
                json={
                    "action": "addNote",
                    "version": 6,
                    "params": {"note": note}
                }
            )
            result = response.json()
            if result.get("error"):
                logger.error(f"Failed to add note: {result['error']}")
                return None
            return result.get("result")
        except Exception as e:
            logger.error(f"Failed to add note: {e}")
            return None
    
    def _update_note(self, note_id: int, fields: Dict[str, str]) -> bool:
        """Update an existing note."""
        try:
            response = requests.post(
                self.url,
                json={
                    "action": "updateNoteFields",
                    "version": 6,
                    "params": {
                        "note": {
                            "id": note_id,
                            "fields": fields
                        }
                    }
                }
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Failed to update note {note_id}: {e}")
            return False
    
    def _find_notes(self, query: str) -> List[int]:
        """Find notes matching a query."""
        try:
            response = requests.post(
                self.url,
                json={
                    "action": "findNotes",
                    "version": 6,
                    "params": {"query": query}
                }
            )
            result = response.json()
            return result.get("result", [])
        except Exception as e:
            logger.error(f"Failed to find notes: {e}")
            return []
    
    def _get_note_info(self, note_ids: List[int]) -> List[Dict[str, Any]]:
        """Get information about notes."""
        try:
            response = requests.post(
                self.url,
                json={
                    "action": "notesInfo",
                    "version": 6,
                    "params": {"notes": note_ids}
                }
            )
            result = response.json()
            return result.get("result", [])
        except Exception as e:
            logger.error(f"Failed to get note info: {e}")
            return []
    
    def _sync(self) -> bool:
        """Trigger Anki sync."""
        try:
            response = requests.post(
                self.url,
                json={"action": "sync", "version": 6}
            )
            return response.status_code == 200
        except Exception:
            return False
    
    def _extract_cards(self, lines: List[str]) -> List[Dict[str, Any]]:
        """Extract cards from markdown lines.
        
        Parses markdown content to extract flashcards, including
        front/back content and tags.
        
        Parameters
        ----------
        lines : List[str]
            Lines from the markdown file
        
        Returns
        -------
        List[Dict[str, Any]]
            List of card dictionaries with 'front', 'back', and 'tags'
        
        Notes
        -----
        Cards are identified by ## headers. Tags can be in multiple
        formats: #tag1, #tag2 or - #tag or bullet lists.
        """
        # Find all H2 headers (card starts)
        card_indices = [i for i, line in enumerate(lines) if line.startswith("## ")]
        if not card_indices:
            return []
        
        card_indices.append(len(lines))  # Add end marker
        
        cards = []
        for i in range(len(card_indices) - 1):
            start = card_indices[i]
            end = card_indices[i + 1]
            
            # Extract card content
            heading = lines[start][3:].strip()  # Remove "## "
            body = lines[start + 1:end]
            
            # First, extract tags from the end of the card
            # Tags are typically at the very end after all content
            tags = []
            
            # Check from the end of body for tag lines
            while body:
                last_line = body[-1].strip()
                
                # Check if this is a tag line
                if last_line.startswith('#'):
                    # Inline format: #tag1, #tag2 or just #tag
                    tag_matches = re.findall(r'#([\w.-]+)', last_line)
                    tags = tag_matches + tags  # Prepend to maintain order
                    body.pop()
                elif last_line.startswith('- #'):
                    # List format: - #tag
                    tag_match = re.search(r'#([\w.-]+)', last_line)
                    if tag_match:
                        tags.insert(0, tag_match.group(1))
                    body.pop()
                elif last_line == '':
                    # Empty line, continue checking
                    body.pop()
                else:
                    # Not a tag line, stop
                    break
            
            # Also parse tags using the original method (for other formats)
            additional_tags, body = self._parse_tags(body)
            tags.extend(additional_tags)
            
            # Remove duplicates while preserving order
            seen = set()
            unique_tags = []
            for tag in tags:
                if tag not in seen:
                    seen.add(tag)
                    unique_tags.append(tag)
            tags = unique_tags
            
            # Split front/back
            front, back = self._split_front_back(heading, body)
            
            # Process math and media
            front = self._process_content(front)
            back = self._process_content(back)
            
            if tags:
                logger.info(f"Extracted card with tags: {tags}")
            else:
                logger.warning(f"No tags found for card: {heading[:50]}...")
            
            cards.append({
                'front': front,
                'back': back,
                'tags': tags
            })
        
        return cards
    
    def _parse_tags(self, body: List[str]) -> Tuple[List[str], List[str]]:
        """Parse tags from card body."""
        tags = []
        filtered = []
        
        for line in body:
            match = TAG_LINE_RE.match(line)
            if match:
                raw_tags = match.group(1)
                # Handle both comma-separated and single tags
                if ',' in raw_tags:
                    # Multiple tags separated by commas
                    for tag in TAG_SPLIT_RE.split(raw_tags):
                        tag = tag.strip().lstrip('#')
                        if tag:
                            tags.append(tag)
                else:
                    # Single tag
                    tag = raw_tags.strip().lstrip('#')
                    if tag:
                        tags.append(tag)
            else:
                filtered.append(line)
        
        return tags, filtered
    
    def _split_front_back(self, heading: str, body: List[str]) -> Tuple[str, str]:
        """Split card into front and back."""
        # Find split marker (% or ---)
        split_idx = None
        for i, line in enumerate(body):
            if line.strip() == "%" or HR_SPLIT_RE.match(line):
                split_idx = i
                break
        
        if split_idx is not None:
            front = heading + "\n" + "\n".join(body[:split_idx]).strip()
            back_lines = body[split_idx + 1:]
            
            # Check if the last line(s) contain tags
            # Tags might be at the very end after the back content
            tag_lines = []
            while back_lines and (
                back_lines[-1].strip().startswith('#') or 
                back_lines[-1].strip().startswith('- #') or
                back_lines[-1].strip() == ''
            ):
                line = back_lines.pop()
                if line.strip():  # Only add non-empty lines
                    tag_lines.insert(0, line)
            
            back = "\n".join(back_lines).strip()
        else:
            front = heading
            back = "\n".join(body).strip()
        
        return front, back
    
    def _process_content(self, text: str) -> str:
        """Process math and media in content."""
        # Remove code fences around math
        text = MATH_FENCE_RE.sub(lambda m: m.group(1), text)
        
        # Convert markdown code blocks to HTML for better Anki rendering
        # This preserves syntax highlighting in Anki
        code_block_pattern = r'```(\w+)?\n(.*?)```'
        def replace_code_block(match):
            lang = match.group(1) or ''
            code = match.group(2)
            # Escape HTML entities in code
            code = code.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            # Use monospace font and preserve whitespace
            return f'<pre><code class="{lang}">{code}</code></pre>'
        
        text = re.sub(code_block_pattern, replace_code_block, text, flags=re.DOTALL)
        
        # Convert inline code to HTML
        text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
        
        # Convert markdown math to MathJax
        text = re.sub(r"\$\$(.*?)\$\$", r"\\[\1\\]", text, flags=re.DOTALL)
        text = re.sub(r"(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)", r"\\(\1\\)", text, flags=re.DOTALL)
        
        # Convert audio links to Anki format
        text = AUDIO_LINK_RE.sub(lambda m: f"[sound:{os.path.basename(m.group(1))}]", text)
        
        # Convert image links to HTML
        def replace_image(match):
            url = match.group(1)
            if url.startswith(("http://", "https://")):
                return f'<img src="{url}">'
            else:
                return f'<img src="{os.path.basename(url)}">'
        
        text = IMAGE_RE.sub(replace_image, text)
        
        return text
    
    def _fields_differ(self, existing: Dict[str, Any], new: Dict[str, str]) -> bool:
        """Check if fields differ between existing and new note."""
        for field, value in new.items():
            if existing.get(field, {}).get('value') != value:
                return True
        return False
    
    def _upload_media_files(self, file_path: Path) -> int:
        """Upload media files referenced in the markdown.
        
        Finds and uploads all audio and image files referenced
        in the markdown content.
        
        Parameters
        ----------
        file_path : Path
            Path to the markdown file
        
        Returns
        -------
        int
            Number of files successfully uploaded
        
        Notes
        -----
        Searches for media files relative to the markdown file
        location and up to 3 parent directories.
        """
        base_dir = file_path.parent
        uploaded = 0
        
        # Read file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all media references
        audio_matches = AUDIO_LINK_RE.findall(content)
        image_matches = IMAGE_RE.findall(content)
        
        all_media = audio_matches + [img for img in image_matches if not img.startswith(("http://", "https://"))]
        
        for media_path in all_media:
            # Try to find the file
            full_path = self._find_media_file(media_path, base_dir)
            if full_path and full_path.exists():
                try:
                    with open(full_path, 'rb') as f:
                        data = f.read()
                    filename = full_path.name
                    if self._store_media_file(filename, data):
                        uploaded += 1
                        logger.debug(f"Uploaded media: {filename}")
                except Exception as e:
                    logger.error(f"Failed to upload {full_path}: {e}")
        
        return uploaded
    
    def _find_media_file(self, relative_path: str, base_dir: Path) -> Optional[Path]:
        """Find a media file by trying different path combinations."""
        # Try direct path first
        direct = Path(relative_path)
        if direct.exists():
            return direct
        
        # Try relative to base directory
        relative = base_dir / relative_path
        if relative.exists():
            return relative
        
        # Try parent directories
        current = base_dir
        for _ in range(3):  # Check up to 3 levels up
            test_path = current / relative_path
            if test_path.exists():
                return test_path
            current = current.parent
        
        return None
    
    def _store_media_file(self, filename: str, data: bytes) -> bool:
        """Store a media file in Anki."""
        try:
            encoded_data = base64.b64encode(data).decode('utf-8')
            response = requests.post(
                self.url,
                json={
                    "action": "storeMediaFile",
                    "version": 6,
                    "params": {
                        "filename": filename,
                        "data": encoded_data
                    }
                }
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Failed to store media file {filename}: {e}")
            return False