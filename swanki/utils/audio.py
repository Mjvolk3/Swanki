"""Audio generation utilities for creating TTS audio from card transcripts.

This module provides functions for generating audio files from flashcards
and document content using OpenAI for transcript generation and ElevenLabs
for text-to-speech conversion. Supports various audio types including card
audio, summary narration, full document reading, and educational lectures.

Functions
---------
generate_card_audio(card, card_index, ...)
    Generate audio for flashcard front/back
generate_summary_audio(summary_text, ...)
    Generate audio for document summary
generate_reading_audio(full_content, ...)
    Generate audio for full document reading
generate_lecture_audio(markdown_files, ...)
    Generate educational lecture-style audio
generate_card_transcript(card, is_front, ...)
    Generate optimized transcript for TTS
chunk_text(text, max_chars)
    Split text into manageable chunks
text_to_speech(text, voice_id, ...)
    Convert text to speech using ElevenLabs
combine_audio(files, output)
    Combine multiple audio files

Constants
---------
DEFAULT_VOICE_ID : str
    Default ElevenLabs voice ID

Examples
--------
>>> from swanki.utils.audio import generate_card_audio
>>> from swanki.models.cards import PlainCard, CardContent
>>> from openai import OpenAI
>>> from pathlib import Path
>>> 
>>> card = PlainCard(
...     front=CardContent(text="What is Python?"),
...     back=CardContent(text="A high-level programming language")
... )
>>> 
>>> client = OpenAI()
>>> api_key = "your-elevenlabs-key"
>>> 
>>> front_file, back_file = generate_card_audio(
...     card=card,
...     card_index=1,
...     page_base="page-1",
...     audio_dir=Path("audio"),
...     openai_client=client,
...     elevenlabs_api_key=api_key
... )
"""
import os
import re
import time
import logging
from pathlib import Path
from typing import List, Optional, Tuple
from dotenv import load_dotenv
from elevenlabs import ElevenLabs, VoiceSettings
from pydub import AudioSegment
import tiktoken
from openai import OpenAI

from ..models.cards import PlainCard
from ..utils.formatting import humanize_citation_key

logger = logging.getLogger(__name__)

# Default ElevenLabs voice ID
DEFAULT_VOICE_ID = "7p1Ofvcwsv7UBPoFNcpI"


def generate_card_transcript(
    card: PlainCard,
    is_front: bool,
    client: OpenAI,
    model: str = "gpt-4o",
    citation_key: Optional[str] = None,
    humanized_citation: Optional[str] = None,
) -> str:
    """Generate audio transcript for a card side.
    
    Creates an optimized transcript for text-to-speech conversion,
    handling different card types (regular vs cloze) and properly
    formatting math expressions and citations.
    
    Parameters
    ----------
    card : PlainCard
        The card to generate transcript for
    is_front : bool
        Whether this is the front (True) or back (False) of the card
    client : OpenAI
        OpenAI client for transcript generation
    model : str, optional
        Model to use for generation (default is "gpt-4o")
    citation_key : str, optional
        Citation key to include in front transcript
    humanized_citation : str, optional
        Pre-humanized citation for consistency across cards
    
    Returns
    -------
    str
        The generated transcript text optimized for TTS
    
    Notes
    -----
    - Cloze deletions are replaced with "mask" for audio
    - Math expressions are converted to natural language
    - Citations are humanized (e.g., @smith2023 -> "Smith, 2023")
    - Different prompts used for question vs answer generation
    
    Examples
    --------
    >>> transcript = generate_card_transcript(
    ...     card=card,
    ...     is_front=True,
    ...     client=openai_client,
    ...     citation_key="einstein1905"
    ... )
    >>> print(transcript)
    'Einstein, 1905: What is the theory of special relativity?'
    """
    # Check if this is a cloze card
    is_cloze = "{{c" in card.front.text
    
    # Get the appropriate text WITHOUT citation first
    if is_front:
        content = card.front.text
        
        # For cloze cards on front, explicitly replace the cloze markers with "blank"
        if is_cloze:
            
            # Use a more sophisticated approach to handle nested braces in math
            # First, let's handle the cloze deletions properly by matching balanced braces
            
            def replace_all_cloze_with_blank(text):
                """Replace all cloze deletions with 'blank', handling nested braces."""
                result = text
                # Keep replacing until no more cloze markers are found
                while '{{c' in result:
                    # Find the start of the next cloze
                    start = result.find('{{c')
                    if start == -1:
                        break
                    
                    # Find the digit and ::
                    colon_pos = result.find('::', start)
                    if colon_pos == -1:
                        break
                    
                    # Now find the matching closing braces
                    # Start after the ::
                    pos = colon_pos + 2
                    brace_count = 2  # We already have {{ open
                    
                    while pos < len(result) and brace_count > 0:
                        if result[pos] == '{':
                            brace_count += 1
                        elif result[pos] == '}':
                            brace_count -= 1
                        pos += 1
                    
                    # Replace the entire cloze with 'blank'
                    if brace_count == 0:
                        result = result[:start] + 'blank' + result[pos:]
                    else:
                        # Malformed cloze, just break to avoid infinite loop
                        break
                
                return result
            
            content = replace_all_cloze_with_blank(content)
        
        # Remove any existing citation to work with clean content
        if citation_key and content.startswith(f"@{citation_key}: "):
            content = content[len(f"@{citation_key}: "):]
        elif humanized_citation and content.startswith(f"{humanized_citation}: "):
            content = content[len(f"{humanized_citation}: "):]
    else:
        # For back of card
        if is_cloze:
            # For cloze cards, read the FULL front text but with cloze markers removed
            # This reveals what was hidden
            content = card.front.text
            
            # Remove the cloze markers to reveal the hidden text
            # Need to handle nested braces in LaTeX properly
            def remove_cloze_markers(match):
                # Extract the content, handling potential nested braces
                cloze_content = match.group(1)
                # Count braces to ensure we get the complete content
                brace_count = 0
                complete_content = cloze_content
                remaining = match.string[match.end():]
                
                # Check if we have unclosed braces
                for char in cloze_content:
                    if char == '{':
                        brace_count += 1
                    elif char == '}':
                        brace_count -= 1
                
                # If we have unclosed braces, we need to continue reading
                if brace_count > 0:
                    for i, char in enumerate(remaining):
                        complete_content += char
                        if char == '{':
                            brace_count += 1
                        elif char == '}':
                            brace_count -= 1
                            if brace_count == -2:  # We've found the closing }}
                                # Remove the extra } we added
                                complete_content = complete_content[:-1]
                                break
                
                return complete_content
            
            # Use more sophisticated replacement that handles nested braces
            content = re.sub(r'\{\{c\d+::(.+?)\}\}(?!\})', remove_cloze_markers, content, flags=re.DOTALL)
            
            # Debug log to verify cloze removal
            if "blank" in content.lower():
                logger.warning(f"'blank' found in cloze back content after processing: {content[:100]}...")
            
            # Remove any existing citation to work with clean content
            if citation_key and content.startswith(f"@{citation_key}: "):
                content = content[len(f"@{citation_key}: "):]
            elif humanized_citation and content.startswith(f"{humanized_citation}: "):
                content = content[len(f"{humanized_citation}: "):]
        else:
            # Regular card - use the back text
            content = card.back.text
    
    # Check if we have an image summary to include
    # For cards with images, we ALWAYS want to include the summary in the audio
    # regardless of where the image is visually placed
    image_summary_for_audio = ""
    image_summary_included = False
    
    # Check if this card has an image at all
    has_image = (card.front.image_path is not None) or (card.back.image_path is not None)
    
    # Log detailed debugging info
    logger.debug(f"Card {card.card_id} - Audio generation debug:")
    logger.debug(f"  Is front: {is_front}")
    logger.debug(f"  Has image: {has_image}")
    logger.debug(f"  Front image path: {card.front.image_path}")
    logger.debug(f"  Back image path: {card.back.image_path}")
    logger.debug(f"  Front image summary: {card.front.image_summary}")
    logger.debug(f"  Back image summary: {card.back.image_summary}")
    
    if is_front:
        # For front audio, only include image summary if image is on the FRONT
        if card.front.image_path and card.front.image_summary:
            image_summary_for_audio = card.front.image_summary
            logger.debug(f"  Using front image summary for front audio")
        elif card.front.image_path and not card.front.image_summary:
            # Image exists but no summary - this is a problem
            logger.error(f"Card {card.card_id} has front image but no image summary for audio")
    else:  # Back audio
        # For back audio, only include image summary if image is on the BACK
        if card.back.image_path and card.back.image_summary:
            image_summary_for_audio = card.back.image_summary
            logger.debug(f"  Using back image summary for back audio")
        elif card.back.image_path and not card.back.image_summary:
            # Image exists but no summary - this is a problem
            logger.error(f"Card {card.card_id} has back image but no image summary for audio")
    
    # NOW add citation prefix before processing
    if (is_front or (not is_front and is_cloze)) and (citation_key or humanized_citation):
        # Use pre-humanized citation if provided, otherwise use raw citation key
        citation_prefix = humanized_citation if humanized_citation else f"@{citation_key}"
        content = f"{citation_prefix}: {content.strip()}"
    
    # Always process through LLM for consistent humanization
    # This ensures math, citations, and image descriptions are all properly formatted
    
    # Add image summary to content AFTER the main content if we have one
    if image_summary_for_audio:
        # Place image description after the main content for better flow
        content = content.strip() + ". Image description: " + image_summary_for_audio
        image_summary_included = True
        logger.debug(f"Card {card.card_id}: Added image summary for audio")
    
    if is_front:
        if is_cloze:
            system_content = (
                "Convert this text to natural speech for audio. "
                "CRITICAL INSTRUCTIONS:\n"
                "1. Say 'blank' exactly where it appears in the text\n"
                "2. Do NOT try to figure out what the blank should be\n"
                "3. If the content includes 'Image description:', you MUST read and humanize it\n"
                "   - Convert technical descriptions to natural language\n"
                "   - Describe visual elements in a way that helps audio-only learners\n"
                "   - Make the description conversational and clear\n"
                "4. Read ALL content in order: image description (if present), then the cloze text\n"
                "5. The image description is crucial for audio-only learners - never skip it\n"
                "\n"
                "For mathematical expressions:\n"
                "- Read them naturally as a mathematician would\n"
                "- Fractions: \\frac{a}{b} as 'a over b', \\frac{1}{2} as 'one half'\n"
                "- Summations: \\sum_{i=1}^n as 'sum from i equals 1 to n'\n"
                "- Products: \\prod_{i=1}^n as 'product from i equals 1 to n'\n"
                "- Integrals: \\int_a^b as 'integral from a to b'\n"
                "- Bold symbols: \\mathbf{w} as 'vector w' or 'bold w'\n"
                "- Functions: f(x, y) as 'f of x and y'\n"
                "- Curly braces: \\{...\\} as 'the quantity...'\n"
                "- Square brackets: [a, b] as 'the interval from a to b'\n"
                "- Subscripts: X_j as 'X sub j', X_{parent} as 'X sub parent', X_i as 'X sub i'\n"
                "- Superscripts: X^2 as 'X squared', X^n as 'X to the n', X^{-1} as 'X inverse'\n"
                "- E[X | Y] as 'expected value of X given Y'\n"
                "- E(w) as 'E of w' (error function notation)\n"
                "- X^T as 'X transpose'\n"
                "- (I - W^T) as 'I minus W transpose'\n"
                "- g_j(f_j(X)) as 'g sub j of f sub j of X'\n"
                "- \\mid or | as 'given' in conditional expressions\n"
                "- \\text{} contents should be read normally\n"
                "- Matrix notation: X_1 to X_6 as 'X one to X six'\n"
                "- Greek letters: \\alpha as 'alpha', \\beta as 'beta', \\mathbf{w} as 'bold omega', etc.\n"
                "- Complex expressions: Break down step by step, e.g., E(\\mathbf{w})=\\frac{1}{2}\\sum_{n=1}^N\\{y(x_n,\\mathbf{w})-t_n\\}^2 as 'E of vector w equals one half times the sum from n equals 1 to N of the quantity y of x sub n and vector w minus t sub n, all squared'\n"
                "\n"
                "Remember: Include ALL content, especially image descriptions"
            )
        else:
            system_content = (
                "Convert this flashcard QUESTION to natural speech for audio. "
                "CRITICAL INSTRUCTIONS:\n"
                "1. This is the FRONT of a flashcard - read ALL content IN THE EXACT ORDER PROVIDED\n"
                "2. DO NOT rearrange the content - read it exactly as given\n"
                "3. If 'Image description:' appears at the end, read it there and humanize it:\n"
                "   - Convert technical descriptions to natural language\n"
                "   - Describe visual elements in a way that helps audio-only learners\n"
                "   - Make the description conversational and clear\n"
                "4. DO NOT answer the question or provide explanations\n"
                "5. DO NOT skip the image description - it's crucial for audio-only learners\n"
                "\n"
                "Example structure: [Question as written]. [Humanized image description if present]\n"
                "\n"
                "FORBIDDEN: Do not answer, explain, or elaborate on the question\n"
                "\n"
                "For mathematical expressions:\n"
                "- Read them naturally as a mathematician would\n"
                "- Subscripts: X_j as 'X sub j', X_{parent} as 'X sub parent', X_i as 'X sub i'\n"
                "- Superscripts: X^2 as 'X squared', X^n as 'X to the n'\n"
                "- E[X | Y] as 'expected value of X given Y'\n"
                "- X^{-1} as 'X inverse' not 'X to the power of minus one'\n"
                "- X^T as 'X transpose'\n"
                "- (I - W^T) as 'I minus W transpose'\n"
                "- (I - W^T)^{-1} as 'the inverse of I minus W transpose'\n"
                "- f_2((I - W^T)^{-1}) as 'f two of the inverse of I minus W transpose'\n"
                "- g_j(f_j(X)) as 'g sub j of f sub j of X'\n"
                "- F(W) as 'F of W'\n"
                "- \\mid or | as 'given' in conditional expressions\n"
                "- \\text{} contents should be read normally\n"
                "- Matrix notation: X_1 to X_6 as 'X one to X six'\n"
                "- \\sum as 'sum', \\prod as 'product', \\int as 'integral'\n"
                "- Greek letters: \\alpha as 'alpha', \\beta as 'beta', etc.\n"
                "- Parentheses in math: read naturally, e.g., \\(F(W)\\) as 'F of W'\n"
                "\n"
                "Remember: This is a QUESTION only - do not provide the answer!"
            )
    else:  # Back of card
        if is_cloze:
            system_content = (
                "Read this complete text naturally for audio. "
                "This is the ANSWER that reveals what was hidden in the blanks. "
                "IMPORTANT: The text has already been processed to remove cloze markers. "
                "Do NOT say 'blank' - read all the words that are present. "
                "Read it as a complete statement with all words revealed.\n\n"
                "CRITICAL: Convert ALL mathematical notation to spoken form:\n"
                "- \\(F(W)\\) → 'F of W'\n"
                "- \\(h(W)=0\\) → 'h of W equals zero'\n" 
                "- \\(E[X_j \\mid X_{pa(j)}]\\) → 'expected value of X sub j given X sub parent of j'\n"
                "- \\(g_j(f_j(X))\\) → 'g sub j of f sub j of X'\n"
                "- \\(\\mathbb{E}[X_j \\mid X_{pa(j)}]\\) → 'expected value of X sub j given X sub parent of j'\n"
                "- Any expression like \\(...\\) or $...$ MUST be converted to words\n"
                "- NEVER output raw LaTeX like '\\(F(W)\\)' - always convert to words\n\n"
                "General rules:\n"
                "- Subscripts: X_j as 'X sub j'\n"
                "- Superscripts: X^2 as 'X squared', X^{-1} as 'X inverse'\n"
                "- Greek letters: \\alpha as 'alpha', \\beta as 'beta', etc.\n"
            )
        else:
            system_content = (
                "Convert this answer to natural speech for audio. "
                "CRITICAL INSTRUCTIONS:\n"
                "1. Read ALL content IN THE EXACT ORDER PROVIDED\n"
                "2. DO NOT rearrange the content - read it exactly as given\n"
                "3. If 'Image description:' appears at the end, read it there and humanize it:\n"
                "   - Convert technical descriptions to natural language\n"
                "   - Describe visual elements in a way that helps audio-only learners\n"
                "   - Humanize any mathematical notation in the description\n"
                "\n"
                "For mathematical expressions:\n"
                "- Read them naturally as a mathematician would\n"
                "- Fractions: \\frac{a}{b} as 'a over b', \\frac{1}{2} as 'one half'\n"
                "- Summations: \\sum_{i=1}^n as 'sum from i equals 1 to n'\n"
                "- Products: \\prod_{i=1}^n as 'product from i equals 1 to n'\n"
                "- Integrals: \\int_a^b as 'integral from a to b'\n"
                "- Bold symbols: \\mathbf{w} as 'vector w' or 'bold w'\n"
                "- Functions: f(x, y) as 'f of x and y'\n"
                "- Curly braces: \\{...\\} as 'the quantity...'\n"
                "- Square brackets: [a, b] as 'the interval from a to b'\n"
                "- Subscripts: X_j as 'X sub j', X_{parent} as 'X sub parent', X_i as 'X sub i'\n"
                "- Superscripts: X^2 as 'X squared', X^n as 'X to the n', X^{-1} as 'X inverse'\n"
                "- E[X | Y] as 'expected value of X given Y'\n"
                "- E(w) as 'E of w' (error function notation)\n"
                "- X^T as 'X transpose'\n"
                "- (I - W^T) as 'I minus W transpose'\n"
                "- g_j(f_j(X)) as 'g sub j of f sub j of X'\n"
                "- \\mid or | as 'given' in conditional expressions\n"
                "- \\text{} contents should be read normally\n"
                "- Matrix notation: X_1 to X_6 as 'X one to X six'\n"
                "- Greek letters: \\alpha as 'alpha', \\beta as 'beta', \\mathbf{w} as 'bold omega', etc.\n"
                "- Complex expressions: Break down step by step, e.g., E(\\mathbf{w})=\\frac{1}{2}\\sum_{n=1}^N\\{y(x_n,\\mathbf{w})-t_n\\}^2 as 'E of vector w equals one half times the sum from n equals 1 to N of the quantity y of x sub n and vector w minus t sub n, all squared'\n"
                "- Use context to determine proper reading"
            )
    
    # Handle chunks for long content
    enc = tiktoken.get_encoding("cl100k_base")
    tokens = enc.encode(content)
    max_chunk = 3000
    out_chunks: List[str] = []
    
    # Log the content being sent to LLM
    logger.info(f"Card {card.card_id} - Sending to LLM:")
    logger.info(f"  Content length: {len(content)} chars")
    logger.info(f"  Content preview: {content[:300]}...")
    logger.info(f"  Contains 'Image description:': {'Yes' if 'Image description:' in content else 'No'}")
    
    for start in range(0, len(tokens), max_chunk):
        chunk = enc.decode(tokens[start : start + max_chunk])
        logger.info(f"  Processing chunk {start//max_chunk + 1}, length: {len(chunk)}")
        
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": chunk},
            ],
            temperature=0.3,  # Lower temperature for more consistent output
            max_tokens=2000,  # Increased to prevent cutoff
        )
        
        response_content = resp.choices[0].message.content.strip()
        out_chunks.append(response_content)
        
        logger.info(f"  LLM response length: {len(response_content)} chars")
        logger.info(f"  Response includes image desc: {'Yes' if 'image' in response_content.lower() else 'No'}")
    
    transcript = "\n\n".join(out_chunks)
    
    # Remove any remaining "Guidance:" or similar phrases
    transcript = re.sub(r"(Question|Answer|Guidance):\s*", "", transcript)
    
    return transcript


def chunk_text(text: str, max_chars: int = 3000) -> List[str]:
    """Split text into chunks without breaking words or sentences.
    
    Intelligently splits text at paragraph and sentence boundaries
    to create chunks suitable for TTS processing.
    
    Parameters
    ----------
    text : str
        Text to split into chunks
    max_chars : int, optional
        Maximum characters per chunk (default is 3000)
    
    Returns
    -------
    List[str]
        List of text chunks
    
    Examples
    --------
    >>> long_text = "This is paragraph one.\n\nThis is paragraph two..." * 100
    >>> chunks = chunk_text(long_text, max_chars=500)
    >>> all(len(chunk) <= 500 for chunk in chunks)
    True
    """
    paragraphs = text.split("\n\n")
    chunks: List[str] = []
    current = ""
    
    for p in paragraphs:
        if len(current) + len(p) + 2 <= max_chars:
            current = (current + "\n\n" + p).strip()
        else:
            if current:
                chunks.append(current)
            if len(p) <= max_chars:
                current = p
            else:
                sentences = re.split(r"(?<=[.!?]) +", p)
                part = ""
                for s in sentences:
                    if len(part) + len(s) + 1 <= max_chars:
                        part = (part + " " + s).strip()
                    else:
                        chunks.append(part)
                        part = s
                if part:
                    chunks.append(part)
                current = ""
    
    if current:
        chunks.append(current)
    
    return chunks


def text_to_speech(
    text: str, 
    voice_id: str, 
    output_path: Path, 
    api_key: str,
    speed: float = 1.0
) -> None:
    """Convert a text chunk to speech and save as MP3.
    
    Uses ElevenLabs API to generate high-quality speech from text.
    
    Parameters
    ----------
    text : str
        Text to convert to speech
    voice_id : str
        ElevenLabs voice ID
    output_path : Path
        Path for output MP3 file
    api_key : str
        ElevenLabs API key
    
    Notes
    -----
    Uses the following voice settings:
    - stability: 0.5
    - similarity_boost: 0.75
    - style: 0.2
    - speaker_boost: True
    - model: eleven_multilingual_v2
    - format: mp3_44100_192
    """
    client = ElevenLabs(api_key=api_key)
    settings = VoiceSettings(
        stability=0.5, 
        similarity_boost=0.75, 
        style=0.2, 
        use_speaker_boost=True
    )
    
    stream = client.text_to_speech.convert(
        text=text,
        voice_id=voice_id,
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_192",
        voice_settings=settings,
    )
    
    data = b"".join(stream) if hasattr(stream, "__iter__") else stream
    
    # Apply speed adjustment if needed
    if speed != 1.0:
        # Save to temp file first
        temp_path = output_path.with_suffix('.temp.mp3')
        with open(temp_path, "wb") as f:
            f.write(data)
        
        # Load audio
        audio = AudioSegment.from_mp3(temp_path)
        
        # Use FFmpeg's atempo filter for high-quality speed adjustment
        # atempo preserves pitch while changing speed
        if speed != 1.0:
            # Build the atempo filter chain
            atempo_filters = []
            remaining_speed = speed
            
            # FFmpeg's atempo filter only accepts values between 0.5 and 2.0
            # For values outside this range, we need to chain multiple atempo filters
            while remaining_speed < 0.5 or remaining_speed > 2.0:
                if remaining_speed < 0.5:
                    atempo_filters.append("atempo=0.5")
                    remaining_speed = remaining_speed / 0.5  # This makes it larger (towards 1.0)
                else:
                    atempo_filters.append("atempo=2.0")
                    remaining_speed = remaining_speed / 2.0  # This makes it smaller (towards 1.0)
            
            # Add the final filter for the remaining speed adjustment
            if remaining_speed != 1.0:
                atempo_filters.append(f"atempo={remaining_speed}")
            
            # Apply the filter chain using FFmpeg
            if atempo_filters:
                filter_chain = ",".join(atempo_filters)
                # Always use FFmpeg for speed adjustment - no fallback
                # Add apad to the filter chain to ensure no cutoff
                full_filter_chain = f"{filter_chain},apad=pad_dur=0.1"
                audio.export(
                    output_path,
                    format="mp3",
                    parameters=[
                        "-filter:a", full_filter_chain,
                        "-avoid_negative_ts", "make_zero",
                        "-loglevel", "error"  # Only show errors to reduce noise
                    ]
                )
            else:
                audio.export(output_path, format="mp3")
        else:
            audio.export(output_path, format="mp3")
        
        # Clean up temp file
        temp_path.unlink()
    else:
        with open(output_path, "wb") as f:
            f.write(data)


def combine_audio(files: List[Path], output: Path, crossfade_ms: int = 200, first_crossfade_ms: Optional[int] = None) -> None:
    """Combine multiple MP3 files into one with smooth transitions.
    
    Merges audio files with crossfade to avoid abrupt transitions.
    
    Parameters
    ----------
    files : List[Path]
        List of MP3 files to combine in order
    output : Path
        Path for combined output file
    crossfade_ms : int, optional
        Crossfade duration in milliseconds (default 200)
    first_crossfade_ms : int, optional
        Crossfade duration for first transition only (default None uses crossfade_ms)
    
    Notes
    -----
    - Uses crossfade between segments
    - Exports at 192k bitrate
    - Requires pydub and ffmpeg
    """
    segments = [AudioSegment.from_mp3(str(f)) for f in files]
    combined = segments[0]
    
    for i, seg in enumerate(segments[1:]):
        # Use special crossfade for first transition if specified
        fade_duration = first_crossfade_ms if i == 0 and first_crossfade_ms is not None else crossfade_ms
        combined = combined.append(seg, crossfade=fade_duration)
    
    combined.export(str(output), format="mp3", bitrate="192k")


def generate_citation_audio(
    citation_key: str,
    output_path: Path,
    elevenlabs_api_key: str,
    openai_client: Optional[OpenAI] = None,
    voice_id: Optional[str] = None,
    speed: float = 1.0,
    use_cache: bool = True,
    max_retries: int = 3,
    min_file_size: int = 1024,  # 1KB minimum
    force_regenerate: bool = False,
    citation_speed_override: Optional[float] = None
) -> Path:
    """Generate audio for a citation key that can be reused across cards.
    
    Creates audio for just the humanized citation, which can be combined
    with card content audio for efficiency. Includes validation and retry
    logic to prevent bad audio from being cached.
    
    Parameters
    ----------
    citation_key : str
        The citation key to convert to audio
    output_path : Path
        Path for the output MP3 file
    elevenlabs_api_key : str
        ElevenLabs API key
    openai_client : OpenAI, optional
        OpenAI client for LLM-based humanization (if None, uses basic humanization)
    voice_id : str, optional
        Voice ID (defaults to DEFAULT_VOICE_ID)
    speed : float, optional
        Audio playback speed multiplier (default 1.0)
    use_cache : bool, optional
        Whether to reuse existing file if it exists (default True)
    max_retries : int, optional
        Maximum number of retry attempts (default 3)
    min_file_size : int, optional
        Minimum valid file size in bytes (default 1024)
    force_regenerate : bool, optional
        Force regeneration even if cached file exists (default False)
    citation_speed_override : float, optional
        Override speed specifically for citation audio (default None uses speed param)
    
    Returns
    -------
    Path
        Path to the generated audio file
    
    Raises
    ------
    RuntimeError
        If audio generation fails after all retries
    
    Notes
    -----
    - Humanizes the citation key for natural speech
    - Validates generated audio files
    - Retries on failure with exponential backoff
    - Logs humanized citation for debugging
    - Caches results to avoid regenerating
    """
    voice_id = voice_id or DEFAULT_VOICE_ID
    
    # Humanize the citation using LLM
    if not openai_client:
        raise ValueError("OpenAI client is required for citation audio generation")
    
    # Use LLM to create natural speech-friendly version
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "Convert citation keys to natural speech for text-to-speech. "
                           "Make it flow naturally as if speaking. Add appropriate pauses with commas. "
                           "Keep it concise but clear. Do not add extra words like 'from' or 'by'."
            },
            {
                "role": "user",
                "content": f"Convert this citation key to natural speech: {citation_key}\n\n"
                           "Examples:\n"
                           "smithMachineLearning2023 -> Smith, Machine Learning, 2023\n"
                           "bishopDeepLearningFoundations2024_deep-learning-revolution -> Bishop, Deep Learning Foundations, 2024, deep learning revolution\n"
                           "johnsonEtAl2022 -> Johnson et al, 2022"
            }
        ],
        temperature=0.3,
        max_tokens=100
    )
    humanized = response.choices[0].message.content.strip()
    
    # Log the humanized citation for debugging
    logger.debug(f"Citation audio generation: '{citation_key}' -> '{humanized}'")
    
    # Check if we need to validate existing cache
    if use_cache and not force_regenerate and output_path.exists():
        # Validate existing file
        if _validate_audio_file(output_path, min_file_size, humanized):
            logger.info(f"Using cached citation audio: {output_path}")
            return output_path
        else:
            logger.warning(f"Cached citation audio failed validation, regenerating: {output_path}")
            output_path.unlink()  # Remove invalid cached file
    
    # Format as a natural sentence for better TTS processing
    # The humanized text now has commas for natural pauses
    # e.g., "Bishop, Deep Learning Foundations, 2024, deep learning revolution"
    citation_text = f"{humanized}:"
    
    # Try to generate audio with retries
    last_error = None
    for attempt in range(max_retries):
        try:
            logger.debug(f"Generating citation audio (attempt {attempt + 1}/{max_retries})")
            
            # Generate audio
            # Use citation speed override if provided, otherwise use regular speed
            citation_speed = citation_speed_override if citation_speed_override is not None else speed
            text_to_speech(
                text=citation_text,
                voice_id=voice_id,
                output_path=output_path,
                api_key=elevenlabs_api_key,
                speed=citation_speed
            )
            
            # Validate the generated file
            if _validate_audio_file(output_path, min_file_size, humanized):
                logger.debug(f"Successfully generated citation audio: {output_path}")
                return output_path
            else:
                logger.warning(f"Generated audio failed validation (attempt {attempt + 1})")
                if output_path.exists():
                    output_path.unlink()
                    
        except Exception as e:
            last_error = e
            logger.error(f"Error generating citation audio (attempt {attempt + 1}): {e}")
            if output_path.exists():
                output_path.unlink()
        
        # Exponential backoff between retries
        if attempt < max_retries - 1:
            wait_time = 2 ** attempt
            logger.info(f"Waiting {wait_time} seconds before retry...")
            time.sleep(wait_time)
    
    # All retries failed
    error_msg = f"Failed to generate valid citation audio after {max_retries} attempts"
    if last_error:
        error_msg += f": {last_error}"
    raise RuntimeError(error_msg)


def _validate_audio_file(
    audio_path: Path, 
    min_size: int = 1024, 
    expected_content: str = ""
) -> bool:
    """Validate an audio file for basic integrity.
    
    Checks that the audio file exists, has reasonable size, and
    can be loaded as valid audio.
    
    Parameters
    ----------
    audio_path : Path
        Path to the audio file to validate
    min_size : int, optional
        Minimum file size in bytes (default 1024)
    expected_content : str, optional
        Expected content for logging (default "")
    
    Returns
    -------
    bool
        True if file is valid, False otherwise
    """
    # Check if file exists
    if not audio_path.exists():
        logger.warning(f"Audio file does not exist: {audio_path}")
        return False
    
    # Check file size
    file_size = audio_path.stat().st_size
    if file_size < min_size:
        logger.warning(f"Audio file too small ({file_size} bytes): {audio_path}")
        return False
    
    # Try to load the audio file to verify it's valid
    try:
        audio = AudioSegment.from_mp3(str(audio_path))
        duration_ms = len(audio)
        
        # Check minimum duration (at least 500ms for a citation)
        if duration_ms < 500:
            logger.warning(f"Audio too short ({duration_ms}ms) for content '{expected_content}': {audio_path}")
            return False
        
        # Check maximum duration (citation shouldn't be longer than 10 seconds)
        if duration_ms > 10000:
            logger.warning(f"Audio too long ({duration_ms}ms) for citation '{expected_content}': {audio_path}")
            return False
        
        logger.debug(f"Audio validation passed: {audio_path} ({duration_ms}ms, {file_size} bytes)")
        return True
        
    except Exception as e:
        logger.error(f"Failed to load audio file {audio_path}: {e}")
        return False


def generate_summary_audio(
    summary_text: str,
    output_path: Path,
    openai_client: OpenAI,
    elevenlabs_api_key: str,
    voice_id: Optional[str] = None,
    model: str = "gpt-4o",
    citation_key: Optional[str] = None,
    speed: float = 1.0,
) -> str:
    """Generate audio for document summary.
    
    Creates narration-style audio optimized for academic summaries,
    with proper handling of technical terms and citations.
    
    Parameters
    ----------
    summary_text : str
        The summary text to convert to audio
    output_path : Path
        Path for the output MP3 file
    openai_client : OpenAI
        OpenAI client for transcript generation
    elevenlabs_api_key : str
        ElevenLabs API key
    voice_id : str, optional
        Voice ID (defaults to DEFAULT_VOICE_ID)
    model : str, optional
        OpenAI model to use (default is "gpt-4o")
    citation_key : str, optional
        Citation key to announce at beginning
    speed : float, optional
        Audio playback speed multiplier (default 1.0)
    
    Returns
    -------
    str
        Filename of the generated audio file
    
    Examples
    --------
    >>> filename = generate_summary_audio(
    ...     summary_text="This paper presents a new algorithm...",
    ...     output_path=Path("summary.mp3"),
    ...     openai_client=client,
    ...     elevenlabs_api_key="key",
    ...     citation_key="smith2023"
    ... )
    >>> print(filename)
    'summary.mp3'
    """
    voice_id = voice_id or DEFAULT_VOICE_ID
    
    # Generate transcript optimized for summary reading
    system_prompt = (
        "You are converting a document summary to audio format. "
        "Follow these rules precisely:\n"
        "1. If there is a citation key, mention it at the beginning\n"
        "2. Speak in a clear, academic tone suitable for summarization\n"
        "3. Convert any math notation to spoken form\n"
        "4. Expand acronyms on first use\n"
        "5. Add natural pauses between main points\n"
        "6. Keep the content informative but accessible\n"
        "7. Never include phrases like 'Summary:' or 'This document...'\n"
    )
    
    user_content = summary_text
    if citation_key:
        humanized_key = humanize_citation_key(citation_key)
        user_content = f"Citation: {humanized_key}\n\n{summary_text}"
    
    # Generate transcript
    response = openai_client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
        temperature=0.3,
        max_tokens=1500,
    )
    
    transcript = response.choices[0].message.content.strip()
    
    # Save transcript for debugging/editing
    transcripts_dir = output_path.parent / "summary_transcript"
    transcripts_dir.mkdir(parents=True, exist_ok=True)
    transcript_path = transcripts_dir / f"{output_path.stem}_transcript.md"
    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(f"# Summary Audio Transcript\n\n")
        if citation_key:
            f.write(f"**Citation Key:** {citation_key}\n\n")
        f.write(f"**Generated Transcript:**\n\n{transcript}\n")
    
    # Generate audio
    chunks = chunk_text(transcript)
    if len(chunks) == 1:
        text_to_speech(chunks[0], voice_id, output_path, elevenlabs_api_key, speed)
    else:
        # Generate chunks and combine
        chunk_paths = []
        for i, chunk in enumerate(chunks):
            # Include citation_key in temp file name to avoid conflicts
            prefix = f"{citation_key}_{output_path.stem}" if citation_key else output_path.stem
            chunk_path = output_path.parent / f"{prefix}_chunk{i}.mp3"
            text_to_speech(chunk, voice_id, chunk_path, elevenlabs_api_key, speed)
            chunk_paths.append(chunk_path)
            time.sleep(1)  # Rate limiting
        
        combine_audio(chunk_paths, output_path)
        # Clean up chunks
        for p in chunk_paths:
            p.unlink()
    
    return output_path.name


def generate_reading_audio(
    full_content: str,
    output_path: Path,
    openai_client: OpenAI,
    elevenlabs_api_key: str,
    voice_id: Optional[str] = None,
    model: str = "gpt-4o",
    citation_key: Optional[str] = None,
    speed: float = 1.0,
) -> str:
    """Generate audio for full document reading.
    
    Creates a complete audio narration of the document, suitable for
    listening to the entire content. Handles long documents by chunking
    and combining audio segments.
    
    Parameters
    ----------
    full_content : str
        The full document content to convert to audio
    output_path : Path
        Path for the output MP3 file
    openai_client : OpenAI
        OpenAI client for transcript generation
    elevenlabs_api_key : str
        ElevenLabs API key
    voice_id : str, optional
        Voice ID (defaults to DEFAULT_VOICE_ID)
    model : str, optional
        OpenAI model to use (default is "gpt-4o")
    citation_key : str, optional
        Citation key to announce at beginning
    speed : float, optional
        Audio playback speed multiplier (default 1.0)
    
    Returns
    -------
    str
        Filename of the generated audio file
    
    Notes
    -----
    - Converts LaTeX and math to natural speech
    - Expands acronyms and technical terms
    - Skips image references but reads captions
    - Processes in 3000-token chunks for stability
    - Audio chunks limited to 2000 chars for quality
    
    Examples
    --------
    >>> filename = generate_reading_audio(
    ...     full_content=document_text,
    ...     output_path=Path("reading.mp3"),
    ...     openai_client=client,
    ...     elevenlabs_api_key="key"
    ... )
    """
    voice_id = voice_id or DEFAULT_VOICE_ID
    
    # Generate transcript optimized for full reading
    system_prompt = (
        "You are converting a full document to audio format for reading aloud. "
        "Follow these rules precisely:\n"
        "1. If there is a citation key, mention it at the beginning\n"
        "2. Convert LaTeX and math notation to natural spoken form\n"
        "3. Expand all acronyms and technical terms\n"
        "4. Skip image references but read figure captions\n"
        "5. Add natural pauses for section breaks\n"
        "6. Maintain academic tone but make it listenable\n"
        "7. Never include markup or formatting instructions\n"
    )
    
    user_content = full_content
    if citation_key:
        humanized_key = humanize_citation_key(citation_key)
        user_content = f"Citation: {humanized_key}\n\n{full_content}"
    
    # Process in chunks due to length
    enc = tiktoken.get_encoding("cl100k_base")
    tokens = enc.encode(user_content)
    max_chunk = 3000
    transcript_chunks = []
    
    for start in range(0, len(tokens), max_chunk):
        chunk = enc.decode(tokens[start : start + max_chunk])
        response = openai_client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": chunk},
            ],
            temperature=0.3,
            max_tokens=1000,
        )
        transcript_chunks.append(response.choices[0].message.content.strip())
    
    full_transcript = "\n\n".join(transcript_chunks)
    
    # Save transcript for debugging/editing
    transcripts_dir = output_path.parent / "full_read"
    transcripts_dir.mkdir(parents=True, exist_ok=True)
    transcript_path = transcripts_dir / f"{output_path.stem}_transcript.md"
    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(f"# Full Reading Audio Transcript\n\n")
        if citation_key:
            f.write(f"**Citation Key:** {citation_key}\n\n")
        f.write(f"**Generated Transcript:**\n\n{full_transcript}\n")
    
    # Generate audio in chunks
    audio_chunks = chunk_text(full_transcript, max_chars=2000)  # Smaller chunks for long content
    chunk_paths = []
    
    for i, chunk in enumerate(audio_chunks):
        # Include citation_key in temp file name to avoid conflicts
        prefix = f"{citation_key}_{output_path.stem}" if citation_key else output_path.stem
        chunk_path = output_path.parent / f"{prefix}_chunk{i}.mp3"
        text_to_speech(chunk, voice_id, chunk_path, elevenlabs_api_key, speed)
        chunk_paths.append(chunk_path)
        time.sleep(1)  # Rate limiting
    
    # Combine all chunks
    combine_audio(chunk_paths, output_path)
    
    # Clean up chunks
    for p in chunk_paths:
        p.unlink()
    
    return output_path.name


def generate_lecture_audio(
    markdown_files: List[Path],
    image_summaries: List[str],
    output_path: Path,
    openai_client: OpenAI,
    elevenlabs_api_key: str,
    voice_id: Optional[str] = None,
    model: str = "gpt-4o",
    citation_key: Optional[str] = None,
    lecture_prompt_config: Optional[dict] = None,
    speed: float = 1.0,
) -> str:
    """Generate educational lecture-style audio from document content.
    
    Creates an engaging educational presentation from the document,
    incorporating image descriptions and emphasizing key concepts.
    Uses higher temperature for more dynamic narration.
    
    Parameters
    ----------
    markdown_files : List[Path]
        List of cleaned markdown file paths in order
    image_summaries : List[str]
        List of image summary strings to embed
    output_path : Path
        Path for the output MP3 file
    openai_client : OpenAI
        OpenAI client for transcript generation
    elevenlabs_api_key : str
        ElevenLabs API key
    voice_id : str, optional
        Voice ID (defaults to DEFAULT_VOICE_ID)
    model : str, optional
        OpenAI model to use (default is "gpt-4o")
    citation_key : str, optional
        Citation key to include in lecture
    speed : float, optional
        Audio playback speed multiplier (default 1.0)
    lecture_prompt_config : dict, optional
        Custom prompt configuration with keys:
        - 'lecture_system': System prompt
        - 'lecture_generation': User prompt template
    
    Returns
    -------
    str
        Filename of the generated audio file
    
    Notes
    -----
    - Embeds image summaries at appropriate locations
    - Uses temperature 0.7 for engaging delivery
    - Processes in 4000-token chunks
    - Supports custom prompts via config
    
    Examples
    --------
    >>> config = {
    ...     'lecture_system': 'You are a professor...',
    ...     'lecture_generation': 'Create a lecture on {content}'
    ... }
    >>> filename = generate_lecture_audio(
    ...     markdown_files=[Path("page1.md"), Path("page2.md")],
    ...     image_summaries=["Figure 1 shows..."],
    ...     output_path=Path("lecture.mp3"),
    ...     openai_client=client,
    ...     elevenlabs_api_key="key",
    ...     lecture_prompt_config=config
    ... )
    """
    voice_id = voice_id or DEFAULT_VOICE_ID
    
    # Prepare content with embedded image summaries
    full_content = ""
    image_idx = 0
    
    for md_file in markdown_files:
        content = md_file.read_text()
        
        # Replace image placeholders with summaries
        while "![" in content and image_idx < len(image_summaries):
            # Find next image reference
            img_start = content.find("![")
            img_end = content.find(")", img_start)
            if img_end > img_start:
                # Insert summary after the image
                before = content[:img_end + 1]
                after = content[img_end + 1:]
                content = f"{before}\n\n{image_summaries[image_idx]}\n\n{after}"
                image_idx += 1
            else:
                break
        
        full_content += content + "\n\n"
    
    # Get prompt configuration
    if lecture_prompt_config:
        system_prompt = lecture_prompt_config.get('lecture_system', 'You are an expert educator.')
        user_template = lecture_prompt_config.get('lecture_generation', 'Create a lecture from: {content}')
    else:
        # Default prompts - focus on clarity and directness
        system_prompt = """You are creating a clear, informative audio presentation of academic content.
Focus on clarity and educational value without unnecessary dramatization.
Start directly with the content without lengthy introductions."""
        user_template = """Create a clear educational presentation from this document.

Guidelines:
1. Begin directly with the main content - no lengthy introductions
2. Use a professional, informative tone
3. Focus on key concepts and findings
4. Avoid theatrical or overly dramatic language
5. End concisely without extended conclusions
6. Mention the citation key naturally at the beginning: {citation_key}

Content to present:
{content}"""
    
    # Format user content
    if citation_key:
        humanized_key = humanize_citation_key(citation_key)
        user_content = user_template.format(
            citation_key=humanized_key,
            content=full_content
        )
    else:
        user_content = user_template.format(content=full_content)
    
    # Process in chunks due to length (like legacy)
    enc = tiktoken.get_encoding("cl100k_base")
    tokens = enc.encode(user_content)
    chunk_size = 4000  # From legacy
    max_output_tokens = 3000  # From legacy
    transcript_chunks = []
    
    for start in range(0, len(tokens), chunk_size):
        chunk = enc.decode(tokens[start : start + chunk_size])
        
        # Format the chunk with the template if it's the first chunk
        if start == 0:
            chunk_content = user_content[:len(chunk)]
        else:
            chunk_content = chunk
            
        response = openai_client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": chunk_content},
            ],
            temperature=0.7,  # From legacy
            max_tokens=max_output_tokens,
        )
        transcript_chunks.append(response.choices[0].message.content.strip())
    
    # Combine transcript chunks
    full_transcript = "\n\n".join(transcript_chunks)
    
    # Save transcript for debugging/editing
    transcripts_dir = output_path.parent / "lecture_transcript"
    transcripts_dir.mkdir(parents=True, exist_ok=True)
    transcript_path = transcripts_dir / f"{output_path.stem}_transcript.md"
    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(f"# Lecture Audio Transcript\n\n")
        if citation_key:
            f.write(f"**Citation Key:** {citation_key}\n\n")
        f.write(f"**Generated Transcript:**\n\n{full_transcript}\n")
    
    # Generate audio in smaller chunks for stability
    audio_chunks = chunk_text(full_transcript, max_chars=2000)
    chunk_paths = []
    
    for i, chunk in enumerate(audio_chunks):
        # Include citation_key in temp file name to avoid conflicts
        prefix = f"{citation_key}_{output_path.stem}" if citation_key else output_path.stem
        chunk_path = output_path.parent / f"{prefix}_chunk{i}.mp3"
        text_to_speech(chunk, voice_id, chunk_path, elevenlabs_api_key, speed)
        chunk_paths.append(chunk_path)
        time.sleep(1)  # Rate limiting
    
    # Combine all chunks
    if len(chunk_paths) == 1:
        # Just rename if single chunk
        chunk_paths[0].rename(output_path)
    else:
        combine_audio(chunk_paths, output_path)
        # Clean up chunks
        for p in chunk_paths:
            p.unlink()
    
    return output_path.name


def generate_card_audio(
    card: PlainCard,
    card_index: int,
    page_base: str,
    audio_dir: Path,
    openai_client: OpenAI,
    elevenlabs_api_key: str,
    voice_id: Optional[str] = None,
    model: str = "gpt-4o",
    citation_key: Optional[str] = None,
    speed: float = 1.0,
    force_regenerate_citation: bool = False,
) -> Tuple[str, Optional[str]]:
    """Generate audio files for both sides of a card.
    
    Creates audio files for flashcard content, handling both regular
    and cloze cards. Cloze cards mask hidden text on front, reveal on back.
    Citation audio is generated separately and always placed first to ensure
    consistent ordering.
    
    Parameters
    ----------
    card : PlainCard
        The card to generate audio for
    card_index : int
        Index of the card (1-based) for naming
    page_base : str
        Base name for the page (e.g., "page-1")
    audio_dir : Path
        Directory to save audio files
    openai_client : OpenAI
        OpenAI client for transcript generation
    elevenlabs_api_key : str
        ElevenLabs API key
    voice_id : str, optional
        Voice ID (defaults to DEFAULT_VOICE_ID)
    model : str, optional
        OpenAI model to use (default is "gpt-4o")
    citation_key : str, optional
        Citation key for file naming and content
    speed : float, optional
        Audio playback speed multiplier (default 1.0)
    force_regenerate_citation : bool, optional
        Force regeneration of citation audio even if cached (default False)
    
    Returns
    -------
    Tuple[str, Optional[str]]
        Tuple of (front_filename, back_filename). Back may be None
        if no back transcript was generated.
    
    Examples
    --------
    >>> front, back = generate_card_audio(
    ...     card=my_card,
    ...     card_index=1,
    ...     page_base="page-1",
    ...     audio_dir=Path("audio"),
    ...     openai_client=client,
    ...     elevenlabs_api_key="key",
    ...     citation_key="doe2024"
    ... )
    >>> print(front)
    'doe2024_a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6_front.mp3'
    >>> print(back)
    'doe2024_a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6_back.mp3'
    
    Notes
    -----
    - Files are named using card UUID for order-independent pairing
    - Citation key is prefixed to avoid conflicts between documents
    - Rate limiting is applied between API calls
    - Large transcripts are chunked and combined
    - Temporary chunk files are cleaned up after combination
    """
    voice_id = voice_id or DEFAULT_VOICE_ID
    
    # Humanize citation key once for consistency
    humanized_citation = humanize_citation_key(citation_key) if citation_key else None
    
    # Log the humanized citation for debugging
    if humanized_citation:
        logger.debug(f"Card {card.card_id} - Using humanized citation: '{humanized_citation}' (from '{citation_key}')")
    
    # Generate transcripts WITHOUT citation for the main content
    # We'll add citation audio separately to ensure it's always first
    front_transcript = generate_card_transcript(
        card, is_front=True, client=openai_client, model=model, 
        citation_key=None,  # Don't include citation in transcript
        humanized_citation=None
    )
    
    # Generate back transcript (for all cards now, including cloze)
    back_transcript = generate_card_transcript(
        card, is_front=False, client=openai_client, model=model, 
        citation_key=None,  # Don't include citation in transcript
        humanized_citation=None
    )
    
    # Store transcripts on the card for validation
    card.audio_front_transcript = front_transcript
    card.audio_back_transcript = back_transcript
    
    # Use card UUID for order-independent audio file naming
    # This ensures audio files always match their cards regardless of ordering
    card_uuid = card.card_id  # This is auto-generated by the model validator
    
    if citation_key:
        front_filename = f"{citation_key}_{card_uuid}_front.mp3"
        back_filename = f"{citation_key}_{card_uuid}_back.mp3"
    else:
        front_filename = f"{card_uuid}_front.mp3"
        back_filename = f"{card_uuid}_back.mp3"
    
    front_path = audio_dir / front_filename
    back_path = audio_dir / back_filename
    
    # Save transcripts to markdown files for debugging
    transcripts_dir = audio_dir.parent / "complementary_transcripts"
    transcripts_dir.mkdir(parents=True, exist_ok=True)
    
    # Save front transcript
    front_transcript_filename = f"{citation_key}_{card_uuid}_front.md" if citation_key else f"{card_uuid}_front.md"
    front_transcript_path = transcripts_dir / front_transcript_filename
    with open(front_transcript_path, "w", encoding="utf-8") as f:
        f.write(f"# Card {card_index} - Front Transcript\n\n")
        f.write(f"**Card ID:** {card_uuid}\n\n")
        f.write(f"**Original Text:**\n{card.front.text}\n\n")
        if card.front.image_path:
            f.write(f"**Image Path:** {card.front.image_path}\n\n")
        if card.front.image_summary:
            f.write(f"**Image Summary:** {card.front.image_summary}\n\n")
        
        # Debug info for image summary inclusion
        f.write(f"**Image Summary Debug:**\n")
        f.write(f"- Has image on front: {card.front.image_path is not None}\n")
        f.write(f"- Has image on back: {card.back.image_path is not None}\n")
        f.write(f"- Front image summary: {'Yes' if card.front.image_summary else 'No'}\n")
        f.write(f"- Back image summary: {'Yes' if card.back.image_summary else 'No'}\n")
        f.write(f"- Image summary included in transcript: {'Yes' if any(phrase in front_transcript for phrase in ['Image description:', 'image description:']) else 'No'}\n\n")
        
        f.write(f"**Generated Transcript:**\n{front_transcript}\n")
        
        # Add the actual citation that was added
        if humanized_citation:
            f.write(f"\n**Citation Added:** {humanized_citation}\n")
    
    # Save back transcript if generated
    if back_transcript:
        back_transcript_filename = f"{citation_key}_{card_uuid}_back.md" if citation_key else f"{card_uuid}_back.md"
        back_transcript_path = transcripts_dir / back_transcript_filename
        with open(back_transcript_path, "w", encoding="utf-8") as f:
            f.write(f"# Card {card_index} - Back Transcript\n\n")
            f.write(f"**Card ID:** {card_uuid}\n\n")
            f.write(f"**Original Text:**\n{card.back.text if not ('{{c' in card.front.text) else card.front.text}\n\n")
            if card.back.image_path:
                f.write(f"**Image Path:** {card.back.image_path}\n\n")
            if card.back.image_summary:
                f.write(f"**Image Summary:** {card.back.image_summary}\n\n")
            f.write(f"**Generated Transcript:**\n{back_transcript}\n")
    
    # Generate citation audio separately to ensure it's always first
    citation_audio_path = None
    if citation_key and humanized_citation:
        # Generate citation audio that can be reused
        citation_audio_path = audio_dir / f"{citation_key}_citation.mp3"
        
        try:
            # Always validate existing citation audio, even if cached
            citation_audio_path = generate_citation_audio(
                citation_key=citation_key,
                output_path=citation_audio_path,
                elevenlabs_api_key=elevenlabs_api_key,
                openai_client=openai_client,
                voice_id=voice_id,
                speed=speed,
                use_cache=True,
                force_regenerate=force_regenerate_citation
            )
        except RuntimeError as e:
            logger.error(f"Failed to generate citation audio for card {card.card_id}: {e}")
            # Continue without citation audio rather than failing all cards
            citation_audio_path = None
            logger.warning(f"Proceeding without citation audio for card {card.card_id}")
    
    # Generate front audio
    front_chunks = chunk_text(front_transcript)
    
    # Check if we need to combine audio (citation + content or multiple chunks)
    needs_combination = citation_audio_path is not None or len(front_chunks) > 1
    
    if not needs_combination:
        # Simple case: single chunk, no citation stitching
        text_to_speech(front_chunks[0], voice_id, front_path, elevenlabs_api_key, speed)
    else:
        # Generate chunks and combine
        chunk_paths = []
        
        # Add citation audio first if we have it
        if citation_audio_path and citation_audio_path.exists():
            chunk_paths.append(citation_audio_path)
        
        # Generate content chunks
        for i, chunk in enumerate(front_chunks):
            # Include citation_key in temp file name to avoid conflicts
            prefix = f"{citation_key}_{page_base}" if citation_key else page_base
            chunk_path = audio_dir / f"{prefix}_{card_index}_front_chunk{i}.mp3"
            text_to_speech(chunk, voice_id, chunk_path, elevenlabs_api_key, speed)
            chunk_paths.append(chunk_path)
            time.sleep(1)  # Rate limiting
        
        # Combine all audio (citation + content)
        combine_audio(chunk_paths, front_path)
        
        # Clean up chunks (but not the cached citation audio)
        for p in chunk_paths:
            if p != citation_audio_path:
                p.unlink()
    
    # Generate back audio for all cards (including cloze)
    if back_transcript:
        time.sleep(1)  # Rate limiting between cards
        
        # Generate back audio
        back_chunks = chunk_text(back_transcript)
        if len(back_chunks) == 1:
            text_to_speech(back_chunks[0], voice_id, back_path, elevenlabs_api_key, speed)
        else:
            # Generate chunks and combine
            chunk_paths = []
            for i, chunk in enumerate(back_chunks):
                # Include citation_key in temp file name to avoid conflicts
                prefix = f"{citation_key}_{page_base}" if citation_key else page_base
                chunk_path = audio_dir / f"{prefix}_{card_index}_back_chunk{i}.mp3"
                text_to_speech(chunk, voice_id, chunk_path, elevenlabs_api_key, speed)
                chunk_paths.append(chunk_path)
                time.sleep(1)  # Rate limiting
            
            combine_audio(chunk_paths, back_path)
            # Clean up chunks
            for p in chunk_paths:
                p.unlink()
        
        return front_filename, back_filename
    else:
        # No back transcript was generated
        return front_filename, None