"""Audio generation utilities for creating TTS audio from card transcripts."""
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
    
    Args:
        card: The card to generate transcript for
        is_front: Whether this is the front (True) or back (False) of the card
        client: OpenAI client
        model: Model to use for generation
        citation_key: Optional citation key to include
        
    Returns:
        The generated transcript text
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
    """Split text into chunks of up to max_chars without breaking words or sentences."""
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
    """Convert a text chunk to speech and save as MP3."""
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
    """Combine multiple MP3 files into one with smooth fades."""
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
    
    Args:
        summary_text: The summary text to convert to audio
        output_path: Path for the output MP3 file
        openai_client: OpenAI client for transcript generation
        elevenlabs_api_key: ElevenLabs API key
        voice_id: Optional voice ID
        model: OpenAI model to use
        citation_key: Optional citation key
        
    Returns:
        Filename of the generated audio
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
            chunk_path = output_path.parent / f"{output_path.stem}_chunk{i}.mp3"
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
    
    Args:
        full_content: The full document content to convert to audio
        output_path: Path for the output MP3 file
        openai_client: OpenAI client for transcript generation
        elevenlabs_api_key: ElevenLabs API key
        voice_id: Optional voice ID
        model: OpenAI model to use
        citation_key: Optional citation key
        
    Returns:
        Filename of the generated audio
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
        chunk_path = output_path.parent / f"{output_path.stem}_chunk{i}.mp3"
        text_to_speech(chunk, voice_id, chunk_path, elevenlabs_api_key)
        chunk_paths.append(chunk_path)
        time.sleep(1)  # Rate limiting
    
    # Combine all chunks
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
) -> Tuple[str, str]:
    """Generate audio files for both sides of a card.
    
    Args:
        card: The card to generate audio for
        card_index: Index of the card (1-based)
        page_base: Base name for the page (e.g., "page-1")
        audio_dir: Directory to save audio files
        openai_client: OpenAI client for transcript generation
        elevenlabs_api_key: ElevenLabs API key
        voice_id: Optional voice ID, defaults to DEFAULT_VOICE_ID
        model: OpenAI model to use
        citation_key: Optional citation key
        
    Returns:
        Tuple of (front_audio_path, back_audio_path) relative to audio_dir
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
            chunk_path = audio_dir / f"{page_base}_{card_index}_front_chunk{i}.mp3"
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
                chunk_path = audio_dir / f"{page_base}_{card_index}_back_chunk{i}.mp3"
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