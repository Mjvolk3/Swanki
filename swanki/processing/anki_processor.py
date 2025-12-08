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
        failed_cards = []  # Track failed cards for summary
        
        for card_idx, card in enumerate(cards):
            # Validate and fix cloze card format before processing
            self._validate_and_fix_cloze_format(card)
            
            # Determine card type
            is_cloze = "{{c" in card['front']
            model_name = "Cloze" if is_cloze else "Basic"
            
            # Process content for Anki (handle audio and convert math)
            front_content = self._prepare_for_anki(card['front'])
            back_content = self._prepare_for_anki(card['back'])
            
            # Prepare fields
            if is_cloze:
                # For cloze cards, put front content in Text and back content in Back Extra
                fields = {
                    "Text": front_content,  # Front already has the cloze text and front audio
                    "Back Extra": back_content  # All back content (including audio) goes in Back Extra
                }
                search_key = "Text"
            else:
                fields = {
                    "Front": front_content,
                    "Back": back_content
                }
                search_key = "Front"
            
            # Check if card exists
            # Escape special characters in the search text
            search_text = fields[search_key]
            # Remove audio tags for search
            search_text = re.sub(r'\[sound:[^\]]+\]', '', search_text).strip()
            # Escape quotes and other special chars
            search_text = search_text.replace('"', '\\"').replace('\\', '\\\\')
            # For cloze cards, search without the cloze markers for better matching
            if is_cloze:
                # Remove cloze markers but keep the text
                search_text = re.sub(r'{{c\d+::([^}]+)}}', r'\1', search_text)
            # Limit search text length to avoid issues
            if len(search_text) > 100:
                search_text = search_text[:100]
            
            query = f'deck:"{deck_name}" {search_key}:"{search_text}"'
            existing_ids = self._find_notes(query)
            
            if not existing_ids:
                # Add new card
                note_id = self._add_note(deck_name, model_name, fields, card['tags'])
                if note_id:
                    cards_added += 1
                    logger.debug(f"Added new card: {card['front'][:50]}...")
                else:
                    # Log failed card with more details
                    card_preview = card['front'].split('\n')[0][:100]  # First line, max 100 chars
                    logger.error(f"Failed to add card #{card_idx + 1}: {card_preview}...")
                    logger.debug(f"Card type: {model_name}, Tags: {card['tags']}")
                    failed_cards.append({
                        'index': card_idx + 1,
                        'preview': card_preview,
                        'type': model_name,
                        'tags': card['tags']
                    })
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
        
        # Report failed cards if any
        if failed_cards:
            logger.warning(f"\n{len(failed_cards)} cards failed to import:")
            for failed in failed_cards:
                logger.warning(f"  Card #{failed['index']}: {failed['preview'][:60]}...")
            logger.info("\nCommon reasons for import failures:")
            logger.info("  - Duplicate cards already in deck")
            logger.info("  - Invalid LaTeX/MathJax formatting")
            logger.info("  - Special characters in content")
            logger.info("  - Missing note type (Basic/Cloze) in Anki")
        
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
                # Extract card preview for better error identification
                card_preview = fields.get('Text', fields.get('Front', 'Unknown card'))
                card_preview = card_preview.split('\n')[0][:80]  # First line, max 80 chars
                logger.error(f"Failed to add note: {result['error']} | Card: {card_preview}...")
                # Log additional details for debugging
                if "duplicate" in result['error'].lower():
                    logger.debug("This appears to be a duplicate card")
                elif "invalid" in result['error'].lower():
                    logger.debug(f"Invalid content - check for special characters or formatting issues")
                    logger.debug(f"Tags: {tags}")
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
                    # List format: - #tag1, #tag2 or - #tag
                    tag_matches = re.findall(r'#([\w.-]+)', last_line)
                    # Prepend all found tags to maintain order
                    tags = tag_matches + tags
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
            
            # Don't process content here - just keep raw markdown
            # Processing will happen later when converting for Anki
            
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
    
    def _prepare_for_anki(self, text: str) -> str:
        """Prepare markdown content for Anki.
        
        Handles:
        1. Extract and convert audio links
        2. Convert LaTeX to MathJax notation
        3. Fix cloze issues
        4. Convert markdown formatting to HTML
        """
        if not text:
            return text
            
        # Step 1: Extract audio links BEFORE any processing
        audio_front_match = re.search(r'\[audio-front\]\(([^)]+)\)', text)
        audio_back_match = re.search(r'\[audio-back\]\(([^)]+)\)', text)
        
        # Remove audio links from text temporarily
        text_without_audio = text
        if audio_front_match:
            text_without_audio = text_without_audio.replace(audio_front_match.group(0), '')
        if audio_back_match:
            text_without_audio = text_without_audio.replace(audio_back_match.group(0), '')
        
        # Step 2: Process the content (math, cloze, etc.)
        processed = self._process_content(text_without_audio.strip())
        
        # Step 3: Add audio links back at the END in Anki format
        # Add BOTH front and back audio if they exist
        if audio_front_match:
            audio_file = os.path.basename(audio_front_match.group(1))
            processed = f"{processed}\n\n[sound:{audio_file}]"
        if audio_back_match:  # Changed from elif to if to process both
            audio_file = os.path.basename(audio_back_match.group(1))
            processed = f"{processed}\n\n[sound:{audio_file}]"
            
        return processed
        
    def _process_content(self, text: str) -> str:
        """Process math and media in content (without audio - handled separately)."""
        # Remove code fences around math
        text = MATH_FENCE_RE.sub(lambda m: m.group(1), text)
        
        # Only detect truly raw LaTeX - not already in MathJax delimiters
        # This should rarely trigger if generation is working correctly
        # Pattern: LaTeX command NOT preceded by \( or $ and NOT followed by common math context
        raw_latex_pattern = r'(?<![\\\$\(])(\\(?:mathbf|mathbb|mathrm|mathcal|operatorname|frac|sqrt|sum|prod|int|lambda|alpha|beta|gamma|delta|epsilon|sigma|theta|phi|psi|omega|Omega|Delta|Sigma|Pi|Lambda|Gamma)\{[^}]+\})'
        
        # Count how many we find for debugging
        raw_matches = re.findall(raw_latex_pattern, text)
        if raw_matches and len(raw_matches) <= 5:  # Only warn for a few, not hundreds
            for match in raw_matches[:5]:
                logger.warning(f"Found potentially raw LaTeX: {match[:30]}...")
        
        # Don't auto-wrap anymore - the warnings are enough
        # If we're getting these warnings, the issue is in generation, not processing
        
        # Fix problematic cloze deletions (including pipe characters)
        text = self._fix_cloze_issues(text)
        
        # Also fix pipe characters in math outside of cloze (for determinants, absolute values)
        # This prevents markdown table parsing issues
        # Only convert pipes that are clearly in math context
        def fix_math_pipes(text):
            # Pattern to find inline math $...$ and display math $$...$$
            inline_math_pattern = r'(?<!\$)\$(?!\$)([^$]+)\$(?!\$)'
            display_math_pattern = r'\$\$([^$]+)\$\$'
            
            def replace_pipes_in_math(match):
                math_content = match.group(1)
                # Replace | with \vert for LaTeX compatibility
                if '|' in math_content:
                    math_content = math_content.replace('|', '\\vert ')
                # Return with original delimiters
                if match.group(0).startswith('$$'):
                    return f'$${math_content}$$'
                else:
                    return f'${math_content}$'
            
            # Fix pipes in display math first (to avoid inline pattern matching parts of display)
            text = re.sub(display_math_pattern, replace_pipes_in_math, text, flags=re.DOTALL)
            # Then fix pipes in inline math
            text = re.sub(inline_math_pattern, replace_pipes_in_math, text)
            
            return text
        
        text = fix_math_pipes(text)
        
        # Convert markdown tables to HTML (before code blocks to avoid converting tables in code)
        text = self._convert_markdown_tables_to_html(text)
        
        # Convert markdown lists to HTML for proper Anki rendering
        # This ensures bullet points are displayed correctly
        text = self._convert_markdown_lists_to_html(text)
        
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

        # Convert markdown bold to HTML strong
        text = re.sub(r'\*\*([^*]+?)\*\*', r'<strong>\1</strong>', text)

        # Convert markdown italic to HTML em (avoid matching **)
        text = re.sub(r'(?<!\*)\*(?!\*)([^*]+?)\*(?!\*)(?!\*)', r'<em>\1</em>', text)

        # Convert markdown math to MathJax
        # For display math, use DOTALL to allow multiline equations
        text = re.sub(r"\$\$(.*?)\$\$", r"\\[\1\\]", text, flags=re.DOTALL)
        # For inline math, DON'T use DOTALL to prevent matching across lines
        # This prevents audio links from being caught inside math delimiters
        text = re.sub(r"(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)", r"\\(\1\\)", text)
        
        # Convert image links to HTML
        def replace_image(match):
            url = match.group(1)
            if url.startswith(("http://", "https://")):
                return f'<img src="{url}">'
            else:
                return f'<img src="{os.path.basename(url)}">'
        
        text = IMAGE_RE.sub(replace_image, text)
        
        return text
    
    def _validate_and_fix_cloze_format(self, card: Dict[str, Any]) -> None:
        """Validate and fix cloze card formatting issues.
        
        Ensures cloze deletions are in the front, not the back.
        This catches cards that were incorrectly generated.
        
        Parameters
        ----------
        card : Dict[str, Any]
            Card dictionary with 'front', 'back', and 'tags'
        """
        # Check if cloze markers are in the wrong place
        has_cloze_in_front = "{{c" in card['front']
        has_cloze_in_back = "{{c" in card['back']
        
        if has_cloze_in_back and not has_cloze_in_front:
            # Misformatted cloze card - cloze is in back instead of front
            logger.warning(f"Fixing misformatted cloze card: cloze markers found in back instead of front")
            
            # Extract cloze content from back
            cloze_pattern = r'\{\{c\d+::(.+?)\}\}'
            cloze_matches = re.findall(cloze_pattern, card['back'], re.DOTALL)
            
            if cloze_matches:
                cloze_content = cloze_matches[0].strip()
                
                # Transform the card based on front content
                if card['front'].endswith('?'):
                    # It's a question - transform to statement with cloze
                    base_text = card['front'].rstrip('?').strip()
                    
                    # Common transformations
                    if re.match(r'^What is the (.+)$', base_text, re.IGNORECASE):
                        card['front'] = re.sub(r'^What is the (.+)$', r'The \1 is {{c1::' + cloze_content + '}}', base_text, flags=re.IGNORECASE)
                    elif re.match(r'^Which (.+)$', base_text, re.IGNORECASE):
                        card['front'] = f"{{{{c1::{cloze_content}}}}} {base_text[6:]}"
                    elif re.match(r'^In (.+), what (.+)$', base_text, re.IGNORECASE):
                        match = re.match(r'^In (.+), what (.+)$', base_text, re.IGNORECASE)
                        card['front'] = f"In {match.group(1)}, {{{{c1::{cloze_content}}}}} {match.group(2)}"
                    else:
                        # Generic transformation
                        card['front'] = f"{base_text} is {{{{c1::{cloze_content}}}}}"
                else:
                    # Not a question - just append cloze
                    card['front'] = f"{card['front']} {{{{c1::{cloze_content}}}}}"
                
                # Clear the back (should only have audio for cloze)
                card['back'] = ""
                logger.info(f"Fixed cloze format - moved to front: {card['front'][:80]}...")
        
        elif has_cloze_in_back and has_cloze_in_front:
            # Both have cloze - remove from back
            logger.warning("Cloze card has markers in both front and back - removing from back")
            card['back'] = re.sub(r'\{\{c\d+::[^}]+\}\}', '', card['back']).strip()
        
        # Check for tables inside cloze deletions
        if has_cloze_in_front:
            # Extract cloze content to check for tables
            cloze_pattern = r'{{c\d+::([^}]+)}}'
            for match in re.finditer(cloze_pattern, card['front']):
                cloze_content = match.group(1)
                # Check if there's a table structure (multiple pipes on same line)
                if '|' in cloze_content:
                    lines = cloze_content.split('\n')
                    for line in lines:
                        if line.count('|') >= 2:
                            logger.warning(f"Table detected inside cloze deletion - this is not supported and may cause rendering issues")
                            logger.warning(f"Problematic cloze content: {match.group(0)[:100]}...")
                            break
    
    def _fix_cloze_issues(self, text: str) -> str:
        """Fix common cloze deletion issues that cause Anki import failures.
        
        Parameters
        ----------
        text : str
            Text containing cloze deletions
            
        Returns
        -------
        str
            Text with fixed cloze deletions
        """
        # Fix multiline cloze deletions
        # Pattern to find cloze that spans multiple lines
        multiline_cloze_pattern = r'({{c\d+::(?:[^}]|\n)*?}})'
        
        def fix_multiline_cloze(match):
            cloze_text = match.group(1)
            # Replace newlines with spaces inside cloze
            fixed_cloze = cloze_text.replace('\n', ' ')
            # Clean up multiple spaces
            fixed_cloze = re.sub(r'\s+', ' ', fixed_cloze)
            return fixed_cloze
        
        text = re.sub(multiline_cloze_pattern, fix_multiline_cloze, text, flags=re.DOTALL)
        
        # Fix pipe characters (|) in cloze deletions for determinant notation
        # These interfere with markdown table parsing and Anki rendering
        # Look for cloze deletions that contain pipes (including those with math)
        # Use a non-greedy match to properly capture content between {{ and }}
        cloze_with_pipes_pattern = r'{{(c\d+::)(.*?)}}'
        
        def fix_pipes_in_cloze(match):
            cloze_marker = match.group(1)
            content = match.group(2)
            
            # Only process if there are pipes in the content
            if '|' not in content:
                return match.group(0)
            
            # Check if the pipes are within math context
            # Look for common math indicators
            # This prevents markdown table parsing issues
            math_indicators = ['$', '\\(', '\\[', '\\mathbf', '\\lambda', '\\mathbb', 
                             '\\mathrm', '\\frac', '\\partial', 'matrix', 'det']
            
            # Check if any math indicator is present
            is_math = any(indicator in content for indicator in math_indicators)
            
            # Convert pipes to \vert for LaTeX/MathJax compatibility
            # This works for both determinants and absolute values
            fixed_content = content.replace('|', '\\vert ')
            
            return f'{{{{{cloze_marker}{fixed_content}}}}}'
        
        text = re.sub(cloze_with_pipes_pattern, fix_pipes_in_cloze, text)
        
        # Fix display math inside cloze deletions
        # Pattern: {{c1::\[...\]}} or \[{{c1::...}}\]
        display_math_in_cloze = r'{{(c\d+::)\\\[(.*?)\\\]}}' 
        text = re.sub(display_math_in_cloze, r'{{\1\\(\2\\)}}', text, flags=re.DOTALL)
        
        # Pattern: \[...{{c1::...}}...\]
        cloze_in_display_math = r'\\\[(.*?){{(c\d+::.*?}})(.*?)\\\]'
        
        def fix_cloze_in_display(match):
            before = match.group(1)
            cloze = match.group(2)
            after = match.group(3)
            # Convert to inline math with cloze
            return f'\\({before}{{{cloze}{after}\\)'
        
        text = re.sub(cloze_in_display_math, fix_cloze_in_display, text, flags=re.DOTALL)
        
        # Fix LaTeX issues inside cloze
        # Add spaces before }} to avoid LaTeX conflicts with cloze terminator
        # This is CRITICAL per Anki documentation - when LaTeX ends with }, need space before }}
        # Simply look for }}} pattern (LaTeX } followed by cloze }}) and add space
        # This pattern is: any character that's a } followed by }}
        text = re.sub(r'}}}', r'} }}', text)
        
        return text
    
    def _convert_latex_to_mathjax(self, text: str) -> str:
        """Convert LaTeX dollar notation to MathJax format for Anki.
        
        Parameters
        ----------
        text : str
            Text containing LaTeX dollar notation
            
        Returns
        -------
        str
            Text with MathJax notation for Anki
        """
        # Convert $...$ to \(...\) for inline math
        text = re.sub(r'(?<!\$)\$(?!\$)(.+?)\$(?!\$)', r'\\(\1\\)', text)
        # Convert $$...$$ to \[...\] for display math
        text = re.sub(r'\$\$(.+?)\$\$', r'\\[\1\\]', text, flags=re.DOTALL)
        
        # Clean up problematic LaTeX that might cause Anki import issues
        # Replace \left( and \right) with regular parentheses in MathJax
        text = text.replace('\\left(', '(').replace('\\right)', ')')
        text = text.replace('\\left[', '[').replace('\\right]', ']')
        text = text.replace('\\left\\{', '\\{').replace('\\right\\}', '\\}')
        
        # Fix spacing issues that might cause problems
        text = re.sub(r'\s+\\mathrm{d}', r'\\,\\mathrm{d}', text)  # Add thin space before differentials
        
        return text
    
    def _convert_markdown_lists_to_html(self, text: str) -> str:
        """Convert markdown lists to HTML for better Anki rendering.
        
        Converts both unordered (- or *) and ordered (1. 2. etc) lists to HTML.
        This ensures proper spacing and indentation in Anki.
        
        Parameters
        ----------
        text : str
            Text containing markdown lists
            
        Returns
        -------
        str
            Text with lists converted to HTML
        """
        lines = text.split('\n')
        result = []
        in_ul = False
        in_ol = False
        
        for line in lines:
            # Check for unordered list item
            if re.match(r'^[-*]\s+', line):
                if not in_ul:
                    if in_ol:
                        result.append('</ol>')
                        in_ol = False
                    result.append('<ul>')
                    in_ul = True
                # Extract the list item content
                item_content = re.sub(r'^[-*]\s+', '', line)
                result.append(f'<li>{item_content}</li>')
            # Check for ordered list item
            elif re.match(r'^\d+\.\s+', line):
                if not in_ol:
                    if in_ul:
                        result.append('</ul>')
                        in_ul = False
                    result.append('<ol>')
                    in_ol = True
                # Extract the list item content
                item_content = re.sub(r'^\d+\.\s+', '', line)
                result.append(f'<li>{item_content}</li>')
            else:
                # Not a list item - close any open lists
                if in_ul:
                    result.append('</ul>')
                    in_ul = False
                if in_ol:
                    result.append('</ol>')
                    in_ol = False
                result.append(line)
        
        # Close any remaining open lists
        if in_ul:
            result.append('</ul>')
        if in_ol:
            result.append('</ol>')
        
        return '\n'.join(result)
    
    def _convert_markdown_tables_to_html(self, text: str) -> str:
        """Convert markdown tables to HTML for Anki rendering.
        
        Note: Tables inside cloze deletions are not supported and will be skipped.
        
        Parameters
        ----------
        text : str
            Text containing markdown tables
            
        Returns
        -------
        str
            Text with HTML tables for Anki
        """
        import markdown
        
        # Split text into lines to process tables separately
        lines = text.split('\n')
        result_lines = []
        in_table = False
        table_lines = []
        in_cloze = False
        
        for i, line in enumerate(lines):
            # Track if we're inside a cloze deletion
            if '{{c' in line:
                in_cloze = True
            if '}}' in line and in_cloze:
                in_cloze = False
            
            # Detect table start/continuation (not in code blocks or cloze)
            if '|' in line and not line.strip().startswith('```') and not in_cloze:
                # Check if this looks like a table row (at least 2 pipes)
                if line.count('|') >= 2:
                    in_table = True
                    table_lines.append(line)
                else:
                    # Not a table, just a line with a pipe
                    if in_table and table_lines:
                        # Process accumulated table
                        table_html = self._process_table_lines(table_lines)
                        result_lines.append(table_html)
                        table_lines = []
                        in_table = False
                    result_lines.append(line)
            elif in_table and (line.strip() == '' or i == len(lines) - 1):
                # End of table - convert and add
                if i == len(lines) - 1 and line.strip() != '':
                    table_lines.append(line)  # Add last line if not empty
                
                if table_lines:
                    table_html = self._process_table_lines(table_lines)
                    result_lines.append(table_html)
                    table_lines = []
                    in_table = False
                
                if line.strip() == '':
                    result_lines.append(line)  # Add the empty line
            else:
                if in_table:
                    # No longer in table
                    if table_lines:
                        table_html = self._process_table_lines(table_lines)
                        result_lines.append(table_html)
                        table_lines = []
                        in_table = False
                result_lines.append(line)
        
        # Handle table at end of text if still accumulating
        if table_lines:
            table_html = self._process_table_lines(table_lines)
            result_lines.append(table_html)
        
        return '\n'.join(result_lines)
    
    def _process_table_lines(self, table_lines: List[str]) -> str:
        """Process accumulated table lines into HTML.
        
        Parameters
        ----------
        table_lines : List[str]
            Lines that form a markdown table
            
        Returns
        -------
        str
            HTML table with Anki-friendly styling
        """
        import markdown
        
        # Join lines to form complete table
        table_md = '\n'.join(table_lines)
        
        # Convert to HTML using python-markdown
        try:
            table_html = markdown.markdown(table_md, extensions=['tables'])
            
            # Add Anki-friendly styling
            table_html = table_html.replace('<table>', 
                '<table style="border-collapse: collapse; margin: 10px auto; width: auto;">')
            table_html = table_html.replace('<thead>', 
                '<thead style="background-color: #f2f2f2;">')
            table_html = table_html.replace('<th>', 
                '<th style="border: 1px solid #ddd; padding: 8px; text-align: left;">')
            table_html = table_html.replace('<td>', 
                '<td style="border: 1px solid #ddd; padding: 8px;">')
            
            # Remove surrounding <p> tags that markdown might add
            table_html = table_html.strip()
            if table_html.startswith('<p>') and table_html.endswith('</p>'):
                table_html = table_html[3:-4]
            
            return table_html
        except Exception as e:
            logger.warning(f"Failed to convert table to HTML: {e}")
            # Return original markdown if conversion fails
            return table_md
    
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