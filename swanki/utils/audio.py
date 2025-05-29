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
from pathlib import Path
from typing import List, Optional, Tuple
from dotenv import load_dotenv
from elevenlabs import ElevenLabs, VoiceSettings
from pydub import AudioSegment
import tiktoken
from openai import OpenAI

from ..models.cards import PlainCard
from ..utils.formatting import humanize_citation_key

# Default ElevenLabs voice ID
DEFAULT_VOICE_ID = "7p1Ofvcwsv7UBPoFNcpI"


def generate_card_transcript(
    card: PlainCard,
    is_front: bool,
    client: OpenAI,
    model: str = "gpt-4o",
    citation_key: Optional[str] = None,
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
    
    # Get the appropriate text
    if is_front:
        content = card.front.text
        # Always prepend citation key for front of card, even if already present
        if citation_key:
            # Remove existing citation if present to avoid duplication
            if content.startswith(f"@{citation_key}:"):
                content = content[len(f"@{citation_key}:"):]
            content = f"@{citation_key}: {content.strip()}"
    else:
        content = card.back.text
    
    # Prepare system message based on card type
    if is_front:
        if is_cloze:
            system_content = (
                "You are converting a cloze deletion card to audio format. "
                "Follow these rules precisely:\n"
                "1. ALWAYS start by speaking the citation naturally if present (e.g., @authorYear becomes 'Author, Year')\n"
                "2. Replace any {{c1::hidden text}} with the word 'mask'\n"
                "3. State the sentence naturally, saying 'mask' where content is hidden\n"
                "4. Speak any math expressions in natural language\n"
                "5. Keep your response concise and academic\n"
                "6. Never include phrases like 'Question:' or 'Guidance:'\n"
                "7. Never explain what you're doing, just provide the transcript\n"
            )
        else:
            system_content = (
                "You are converting a flashcard question to audio format. "
                "Follow these rules precisely:\n"
                "1. ALWAYS start by speaking the citation naturally if present (e.g., @authorYear becomes 'Author, Year')\n"
                "2. State only the question without any introductory phrases\n"
                "3. Speak any math expressions in natural language\n"
                "4. Keep your response concise and academic\n"
                "5. Never include phrases like 'Question:' or 'Guidance:'\n"
                "6. Never explain what you're doing, just provide the transcript\n"
            )
    else:  # Back of card
        if is_cloze:
            system_content = (
                "You are providing the answer to a cloze deletion card. "
                "Follow these rules precisely:\n"
                "1. Do NOT restate the question or cite the source again\n"
                "2. Simply state what the hidden text is: 'The missing word is...'\n"
                "3. Speak any math expressions in natural language\n"
                "4. Keep your response very brief - just the missing text\n"
                "5. Never include phrases like 'Answer:' or 'Guidance:'\n"
                "6. Never explain what you're doing, just provide the transcript\n"
            )
        else:
            system_content = (
                "You are providing the answer to a flashcard question. "
                "Follow these rules precisely:\n"
                "1. Do NOT restate the question or cite the source again\n"
                "2. Begin directly with the answer\n"
                "3. Speak any math expressions in natural language\n"
                "4. Keep your response concise and academic\n"
                "5. Never include phrases like 'Answer:' or 'Guidance:'\n"
                "6. Never explain what you're doing, just provide the transcript\n"
                "7. Never start with phrases like 'In the study...' or 'The research shows...'\n"
            )
    
    # Handle chunks for long content
    enc = tiktoken.get_encoding("cl100k_base")
    tokens = enc.encode(content)
    max_chunk = 3000
    out_chunks: List[str] = []
    
    for start in range(0, len(tokens), max_chunk):
        chunk = enc.decode(tokens[start : start + max_chunk])
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": chunk},
            ],
            temperature=0.3,  # Lower temperature for more consistent output
            max_tokens=1000,
        )
        out_chunks.append(resp.choices[0].message.content.strip())
    
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
    api_key: str
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
    with open(output_path, "wb") as f:
        f.write(data)


def combine_audio(files: List[Path], output: Path) -> None:
    """Combine multiple MP3 files into one with smooth transitions.
    
    Merges audio files with crossfade to avoid abrupt transitions.
    
    Parameters
    ----------
    files : List[Path]
        List of MP3 files to combine in order
    output : Path
        Path for combined output file
    
    Notes
    -----
    - Uses 200ms crossfade between segments
    - Exports at 192k bitrate
    - Requires pydub and ffmpeg
    """
    segments = [AudioSegment.from_mp3(str(f)) for f in files]
    combined = segments[0]
    
    for seg in segments[1:]:
        combined = combined.append(seg, crossfade=200)
    
    combined.export(str(output), format="mp3", bitrate="192k")


def generate_summary_audio(
    summary_text: str,
    output_path: Path,
    openai_client: OpenAI,
    elevenlabs_api_key: str,
    voice_id: Optional[str] = None,
    model: str = "gpt-4o",
    citation_key: Optional[str] = None,
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
    
    # Generate audio
    chunks = chunk_text(transcript)
    if len(chunks) == 1:
        text_to_speech(chunks[0], voice_id, output_path, elevenlabs_api_key)
    else:
        # Generate chunks and combine
        chunk_paths = []
        for i, chunk in enumerate(chunks):
            # Include citation_key in temp file name to avoid conflicts
            prefix = f"{citation_key}_{output_path.stem}" if citation_key else output_path.stem
            chunk_path = output_path.parent / f"{prefix}_chunk{i}.mp3"
            text_to_speech(chunk, voice_id, chunk_path, elevenlabs_api_key)
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
    
    # Generate audio in chunks
    audio_chunks = chunk_text(full_transcript, max_chars=2000)  # Smaller chunks for long content
    chunk_paths = []
    
    for i, chunk in enumerate(audio_chunks):
        # Include citation_key in temp file name to avoid conflicts
        prefix = f"{citation_key}_{output_path.stem}" if citation_key else output_path.stem
        chunk_path = output_path.parent / f"{prefix}_chunk{i}.mp3"
        text_to_speech(chunk, voice_id, chunk_path, elevenlabs_api_key)
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
    
    # Generate audio in smaller chunks for stability
    audio_chunks = chunk_text(full_transcript, max_chars=2000)
    chunk_paths = []
    
    for i, chunk in enumerate(audio_chunks):
        # Include citation_key in temp file name to avoid conflicts
        prefix = f"{citation_key}_{output_path.stem}" if citation_key else output_path.stem
        chunk_path = output_path.parent / f"{prefix}_chunk{i}.mp3"
        text_to_speech(chunk, voice_id, chunk_path, elevenlabs_api_key)
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
) -> Tuple[str, Optional[str]]:
    """Generate audio files for both sides of a card.
    
    Creates audio files for flashcard content, handling both regular
    and cloze cards appropriately. Cloze cards only generate front audio.
    
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
    
    Returns
    -------
    Tuple[str, Optional[str]]
        Tuple of (front_filename, back_filename). For cloze cards,
        back_filename is None.
    
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
    'doe2024_page-1_1_front.mp3'
    >>> print(back)
    'doe2024_page-1_1_back.mp3'
    
    Notes
    -----
    - Files are named with citation key prefix to avoid conflicts
    - Rate limiting is applied between API calls
    - Large transcripts are chunked and combined
    - Temporary chunk files are cleaned up after combination
    """
    voice_id = voice_id or DEFAULT_VOICE_ID
    
    # Check if this is a cloze card
    is_cloze = "{{c" in card.front.text or "{c1::" in card.front.text
    
    # Generate transcripts
    front_transcript = generate_card_transcript(
        card, is_front=True, client=openai_client, model=model, citation_key=citation_key
    )
    
    # Only generate back transcript for non-cloze cards
    back_transcript = None
    if not is_cloze:
        back_transcript = generate_card_transcript(
            card, is_front=False, client=openai_client, model=model, citation_key=citation_key
        )
    
    # Generate audio files with citation key prefix to avoid conflicts
    if citation_key:
        front_filename = f"{citation_key}_{page_base}_{card_index}_front.mp3"
        back_filename = f"{citation_key}_{page_base}_{card_index}_back.mp3"
    else:
        front_filename = f"{page_base}_{card_index}_front.mp3"
        back_filename = f"{page_base}_{card_index}_back.mp3"
    
    front_path = audio_dir / front_filename
    back_path = audio_dir / back_filename
    
    # Generate front audio
    front_chunks = chunk_text(front_transcript)
    if len(front_chunks) == 1:
        text_to_speech(front_chunks[0], voice_id, front_path, elevenlabs_api_key)
    else:
        # Generate chunks and combine
        chunk_paths = []
        for i, chunk in enumerate(front_chunks):
            # Include citation_key in temp file name to avoid conflicts
            prefix = f"{citation_key}_{page_base}" if citation_key else page_base
            chunk_path = audio_dir / f"{prefix}_{card_index}_front_chunk{i}.mp3"
            text_to_speech(chunk, voice_id, chunk_path, elevenlabs_api_key)
            chunk_paths.append(chunk_path)
            time.sleep(1)  # Rate limiting
        
        combine_audio(chunk_paths, front_path)
        # Clean up chunks
        for p in chunk_paths:
            p.unlink()
    
    # Only generate back audio for non-cloze cards
    if not is_cloze:
        time.sleep(1)  # Rate limiting between cards
        
        # Generate back audio
        back_chunks = chunk_text(back_transcript)
        if len(back_chunks) == 1:
            text_to_speech(back_chunks[0], voice_id, back_path, elevenlabs_api_key)
        else:
            # Generate chunks and combine
            chunk_paths = []
            for i, chunk in enumerate(back_chunks):
                # Include citation_key in temp file name to avoid conflicts
                prefix = f"{citation_key}_{page_base}" if citation_key else page_base
                chunk_path = audio_dir / f"{prefix}_{card_index}_back_chunk{i}.mp3"
                text_to_speech(chunk, voice_id, chunk_path, elevenlabs_api_key)
                chunk_paths.append(chunk_path)
                time.sleep(1)  # Rate limiting
            
            combine_audio(chunk_paths, back_path)
            # Clean up chunks
            for p in chunk_paths:
                p.unlink()
    else:
        # For cloze cards, return None for back filename
        back_filename = None
    
    return front_filename, back_filename