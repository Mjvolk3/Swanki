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


# ── Module-level card-processing functions ──────────────────────────────
# These have no dependency on AnkiConnect (no host/port/url).
# AnkiProcessor methods delegate to these so both AnkiConnect and
# ApkgExporter can share the same parsing/formatting logic.


def parse_tags(body: List[str]) -> Tuple[List[str], List[str]]:
    """Parse tags from card body lines.

    Parameters
    ----------
    body : List[str]
        Lines of a card body
    Returns
    -------
    Tuple[List[str], List[str]]
        (tags, filtered_body) where filtered_body has tag lines removed
    """
    tags = []
    filtered = []
    for line in body:
        match = TAG_LINE_RE.match(line)
        if match:
            raw_tags = match.group(1)
            if ',' in raw_tags:
                for tag in TAG_SPLIT_RE.split(raw_tags):
                    tag = tag.strip().lstrip('#')
                    if tag:
                        tags.append(tag)
            else:
                tag = raw_tags.strip().lstrip('#')
                if tag:
                    tags.append(tag)
        else:
            filtered.append(line)
    return tags, filtered


def split_front_back(heading: str, body: List[str]) -> Tuple[str, str]:
    """Split card into front and back content.

    Parameters
    ----------
    heading : str
        Card heading text (without ``## `` prefix)
    body : List[str]
        Card body lines

    Returns
    -------
    Tuple[str, str]
        (front, back)
    """
    split_idx = None
    for i, line in enumerate(body):
        if line.strip() == "%" or HR_SPLIT_RE.match(line):
            split_idx = i
            break

    if split_idx is not None:
        front = heading + "\n" + "\n".join(body[:split_idx]).strip()
        back_lines = body[split_idx + 1:]
        tag_lines = []
        while back_lines and (
            back_lines[-1].strip().startswith('#')
            or back_lines[-1].strip().startswith('- #')
            or back_lines[-1].strip() == ''
        ):
            line = back_lines.pop()
            if line.strip():
                tag_lines.insert(0, line)
        back = "\n".join(back_lines).strip()
    else:
        front = heading
        back = "\n".join(body).strip()

    return front, back


def extract_cards(lines: List[str]) -> List[Dict[str, Any]]:
    """Extract cards from markdown lines.

    Parameters
    ----------
    lines : List[str]
        Lines from a markdown file

    Returns
    -------
    List[Dict[str, Any]]
        Card dicts with 'front', 'back', and 'tags' keys
    """
    card_indices = [i for i, line in enumerate(lines) if line.startswith("## ")]
    if not card_indices:
        return []

    card_indices.append(len(lines))

    cards = []
    for i in range(len(card_indices) - 1):
        start = card_indices[i]
        end = card_indices[i + 1]

        heading = lines[start][3:].strip()
        body = lines[start + 1:end]

        tags = []
        while body:
            last_line = body[-1].strip()
            if last_line.startswith('#'):
                tag_matches = re.findall(r'#([\w.-]+)', last_line)
                tags = tag_matches + tags
                body.pop()
            elif last_line.startswith('- #'):
                tag_matches = re.findall(r'#([\w.-]+)', last_line)
                tags = tag_matches + tags
                body.pop()
            elif last_line == '':
                body.pop()
            else:
                break

        additional_tags, body = parse_tags(body)
        tags.extend(additional_tags)

        seen: Set[str] = set()
        unique_tags = []
        for tag in tags:
            if tag not in seen:
                seen.add(tag)
                unique_tags.append(tag)
        tags = unique_tags

        front, back = split_front_back(heading, body)

        if tags:
            logger.info(f"Extracted card with tags: {tags}")
        else:
            logger.warning(f"No tags found for card: {heading[:50]}...")

        cards.append({'front': front, 'back': back, 'tags': tags})

    return cards


def validate_and_fix_cloze_format(card: Dict[str, Any]) -> None:
    """Validate and fix cloze card formatting issues in-place.

    Parameters
    ----------
    card : Dict[str, Any]
        Card dict with 'front', 'back', 'tags'
    """
    has_cloze_in_front = "{{c" in card['front']
    has_cloze_in_back = "{{c" in card['back']

    if has_cloze_in_back and not has_cloze_in_front:
        logger.warning("Fixing misformatted cloze card: cloze markers found in back instead of front")
        cloze_pattern = r'\{\{c\d+::(.+?)\}\}'
        cloze_matches = re.findall(cloze_pattern, card['back'], re.DOTALL)
        if cloze_matches:
            cloze_content = cloze_matches[0].strip()
            if card['front'].endswith('?'):
                base_text = card['front'].rstrip('?').strip()
                if re.match(r'^What is the (.+)$', base_text, re.IGNORECASE):
                    card['front'] = re.sub(
                        r'^What is the (.+)$',
                        r'The \1 is {{c1::' + cloze_content + '}}',
                        base_text, flags=re.IGNORECASE,
                    )
                elif re.match(r'^Which (.+)$', base_text, re.IGNORECASE):
                    card['front'] = f"{{{{c1::{cloze_content}}}}} {base_text[6:]}"
                elif re.match(r'^In (.+), what (.+)$', base_text, re.IGNORECASE):
                    match = re.match(r'^In (.+), what (.+)$', base_text, re.IGNORECASE)
                    card['front'] = f"In {match.group(1)}, {{{{c1::{cloze_content}}}}} {match.group(2)}"
                else:
                    card['front'] = f"{base_text} is {{{{c1::{cloze_content}}}}}"
            else:
                card['front'] = f"{card['front']} {{{{c1::{cloze_content}}}}}"
            card['back'] = ""
            logger.info(f"Fixed cloze format - moved to front: {card['front'][:80]}...")

    elif has_cloze_in_back and has_cloze_in_front:
        logger.warning("Cloze card has markers in both front and back - removing from back")
        card['back'] = re.sub(r'\{\{c\d+::[^}]+\}\}', '', card['back']).strip()

    if has_cloze_in_front:
        cloze_pattern = r'{{c\d+::([^}]+)}}'
        for match in re.finditer(cloze_pattern, card['front']):
            cloze_content = match.group(1)
            if '|' in cloze_content:
                for line in cloze_content.split('\n'):
                    if line.count('|') >= 2:
                        logger.warning("Table detected inside cloze deletion - may cause rendering issues")
                        logger.warning(f"Problematic cloze content: {match.group(0)[:100]}...")
                        break


def fix_cloze_issues(text: str) -> str:
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
    multiline_cloze_pattern = r'({{c\d+::(?:[^}]|\n)*?}})'

    def fix_multiline_cloze(match):
        cloze_text = match.group(1)
        fixed_cloze = cloze_text.replace('\n', ' ')
        fixed_cloze = re.sub(r'\s+', ' ', fixed_cloze)
        return fixed_cloze

    text = re.sub(multiline_cloze_pattern, fix_multiline_cloze, text, flags=re.DOTALL)

    cloze_with_pipes_pattern = r'{{(c\d+::)(.*?)}}'

    def fix_pipes_in_cloze(match):
        cloze_marker = match.group(1)
        content = match.group(2)
        if '|' not in content:
            return match.group(0)
        fixed_content = content.replace('|', '\\vert ')
        return f'{{{{{cloze_marker}{fixed_content}}}}}'

    text = re.sub(cloze_with_pipes_pattern, fix_pipes_in_cloze, text)

    display_math_in_cloze = r'{{(c\d+::)\\\[(.*?)\\\]}}'
    text = re.sub(display_math_in_cloze, r'{{\1\\(\2\\)}}', text, flags=re.DOTALL)

    cloze_in_display_math = r'\\\[(.*?){{(c\d+::.*?}})(.*?)\\\]'

    def fix_cloze_in_display(match):
        before = match.group(1)
        cloze = match.group(2)
        after = match.group(3)
        return f'\\({before}{{{cloze}{after}\\)'

    text = re.sub(cloze_in_display_math, fix_cloze_in_display, text, flags=re.DOTALL)

    text = re.sub(r'}}}', r'} }}', text)

    return text


def process_table_lines(table_lines: List[str]) -> str:
    """Convert markdown table lines to styled HTML.

    Parameters
    ----------
    table_lines : List[str]
        Lines forming a markdown table

    Returns
    -------
    str
        HTML table with Anki-friendly styling
    """
    import markdown

    table_md = '\n'.join(table_lines)
    try:
        table_html = markdown.markdown(table_md, extensions=['tables'])
        table_html = table_html.replace(
            '<table>',
            '<table style="border-collapse: collapse; margin: 10px auto; width: auto;">',
        )
        table_html = table_html.replace('<thead>', '<thead style="background-color: #f2f2f2;">')
        table_html = table_html.replace(
            '<th>', '<th style="border: 1px solid #ddd; padding: 8px; text-align: left;">'
        )
        table_html = table_html.replace('<td>', '<td style="border: 1px solid #ddd; padding: 8px;">')
        table_html = table_html.strip()
        if table_html.startswith('<p>') and table_html.endswith('</p>'):
            table_html = table_html[3:-4]
        return table_html
    except Exception as e:
        logger.warning(f"Failed to convert table to HTML: {e}")
        return table_md


def convert_markdown_tables_to_html(text: str) -> str:
    """Convert markdown tables in text to styled HTML.

    Parameters
    ----------
    text : str
        Text potentially containing markdown tables

    Returns
    -------
    str
        Text with tables converted to HTML
    """
    lines = text.split('\n')
    result_lines = []
    in_table = False
    table_buf: List[str] = []
    in_cloze = False

    for i, line in enumerate(lines):
        if '{{c' in line:
            in_cloze = True
        if '}}' in line and in_cloze:
            in_cloze = False

        if '|' in line and not line.strip().startswith('```') and not in_cloze:
            if line.count('|') >= 2:
                in_table = True
                table_buf.append(line)
            else:
                if in_table and table_buf:
                    result_lines.append(process_table_lines(table_buf))
                    table_buf = []
                    in_table = False
                result_lines.append(line)
        elif in_table and (line.strip() == '' or i == len(lines) - 1):
            if i == len(lines) - 1 and line.strip() != '':
                table_buf.append(line)
            if table_buf:
                result_lines.append(process_table_lines(table_buf))
                table_buf = []
                in_table = False
            if line.strip() == '':
                result_lines.append(line)
        else:
            if in_table:
                if table_buf:
                    result_lines.append(process_table_lines(table_buf))
                    table_buf = []
                    in_table = False
            result_lines.append(line)

    if table_buf:
        result_lines.append(process_table_lines(table_buf))

    return '\n'.join(result_lines)


def convert_markdown_lists_to_html(text: str) -> str:
    """Convert markdown lists to HTML for Anki rendering.

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
        if re.match(r'^[-*]\s+', line):
            if not in_ul:
                if in_ol:
                    result.append('</ol>')
                    in_ol = False
                result.append('<ul>')
                in_ul = True
            item_content = re.sub(r'^[-*]\s+', '', line)
            result.append(f'<li>{item_content}</li>')
        elif re.match(r'^\d+\.\s+', line):
            if not in_ol:
                if in_ul:
                    result.append('</ul>')
                    in_ul = False
                result.append('<ol>')
                in_ol = True
            item_content = re.sub(r'^\d+\.\s+', '', line)
            result.append(f'<li>{item_content}</li>')
        else:
            if in_ul:
                result.append('</ul>')
                in_ul = False
            if in_ol:
                result.append('</ol>')
                in_ol = False
            result.append(line)

    if in_ul:
        result.append('</ul>')
    if in_ol:
        result.append('</ol>')

    return '\n'.join(result)


def process_content(text: str) -> str:
    """Process math, media, and formatting in content for Anki.

    Parameters
    ----------
    text : str
        Raw card content

    Returns
    -------
    str
        Content processed for Anki (tables, lists, math, images, code, cloze fixes)
    """
    text = MATH_FENCE_RE.sub(lambda m: m.group(1), text)

    raw_latex_pattern = r'(?<![\\\$\(])(\\(?:mathbf|mathbb|mathrm|mathcal|operatorname|frac|sqrt|sum|prod|int|lambda|alpha|beta|gamma|delta|epsilon|sigma|theta|phi|psi|omega|Omega|Delta|Sigma|Pi|Lambda|Gamma)\{[^}]+\})'
    raw_matches = re.findall(raw_latex_pattern, text)
    if raw_matches and len(raw_matches) <= 5:
        for match in raw_matches[:5]:
            logger.warning(f"Found potentially raw LaTeX: {match[:30]}...")

    text = fix_cloze_issues(text)

    def fix_math_pipes(t):
        inline_math_pattern = r'(?<!\$)\$(?!\$)([^$]+)\$(?!\$)'
        display_math_pattern = r'\$\$([^$]+)\$\$'

        def replace_pipes_in_math(m):
            math_content = m.group(1)
            if '|' in math_content:
                math_content = math_content.replace('|', '\\vert ')
            if m.group(0).startswith('$$'):
                return f'$${math_content}$$'
            return f'${math_content}$'

        t = re.sub(display_math_pattern, replace_pipes_in_math, t, flags=re.DOTALL)
        t = re.sub(inline_math_pattern, replace_pipes_in_math, t)
        return t

    text = fix_math_pipes(text)

    text = convert_markdown_tables_to_html(text)
    text = convert_markdown_lists_to_html(text)

    code_block_pattern = r'```(\w+)?\n(.*?)```'

    def replace_code_block(match):
        lang = match.group(1) or ''
        code = match.group(2)
        code = code.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        return f'<pre><code class="{lang}">{code}</code></pre>'

    text = re.sub(code_block_pattern, replace_code_block, text, flags=re.DOTALL)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    text = re.sub(r'\*\*([^*]+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'(?<!\*)\*(?!\*)([^*]+?)\*(?!\*)(?!\*)', r'<em>\1</em>', text)
    text = re.sub(r"\$\$(.*?)\$\$", r"\\[\1\\]", text, flags=re.DOTALL)
    text = re.sub(r"(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)", r"\\(\1\\)", text)

    def replace_image(match):
        url = match.group(1)
        if url.startswith(("http://", "https://")):
            return f'<img src="{url}">'
        return f'<img src="{os.path.basename(url)}">'

    text = IMAGE_RE.sub(replace_image, text)

    return text


def prepare_for_anki(text: str) -> str:
    """Prepare markdown content for Anki (audio extraction + content processing).

    Parameters
    ----------
    text : str
        Raw card text potentially containing audio links

    Returns
    -------
    str
        Processed text ready for Anki
    """
    if not text:
        return text

    audio_front_match = re.search(r'\[audio-front\]\(([^)]+)\)', text)
    audio_back_match = re.search(r'\[audio-back\]\(([^)]+)\)', text)

    text_without_audio = text
    if audio_front_match:
        text_without_audio = text_without_audio.replace(audio_front_match.group(0), '')
    if audio_back_match:
        text_without_audio = text_without_audio.replace(audio_back_match.group(0), '')

    processed = process_content(text_without_audio.strip())

    if audio_front_match:
        audio_file = os.path.basename(audio_front_match.group(1))
        processed = f"{processed}\n\n[sound:{audio_file}]"
    if audio_back_match:
        audio_file = os.path.basename(audio_back_match.group(1))
        processed = f"{processed}\n\n[sound:{audio_file}]"

    return processed


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
        return extract_cards(lines)
    
    def _parse_tags(self, body: List[str]) -> Tuple[List[str], List[str]]:
        return parse_tags(body)
    
    def _split_front_back(self, heading: str, body: List[str]) -> Tuple[str, str]:
        return split_front_back(heading, body)
    
    def _prepare_for_anki(self, text: str) -> str:
        return prepare_for_anki(text)
        
    def _process_content(self, text: str) -> str:
        return process_content(text)
    
    def _validate_and_fix_cloze_format(self, card: Dict[str, Any]) -> None:
        validate_and_fix_cloze_format(card)
    
    def _fix_cloze_issues(self, text: str) -> str:
        return fix_cloze_issues(text)
    
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
        return convert_markdown_lists_to_html(text)
    
    def _convert_markdown_tables_to_html(self, text: str) -> str:
        return convert_markdown_tables_to_html(text)
    
    def _process_table_lines(self, table_lines: List[str]) -> str:
        return process_table_lines(table_lines)
    
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