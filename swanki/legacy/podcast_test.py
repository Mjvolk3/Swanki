import os
from dotenv import load_dotenv
from openai import OpenAI
from elevenlabs.client import ElevenLabs
from pydub import AudioSegment
import time

# Load environment variables
dotenv_path = os.path.join(os.getcwd(), ".env")
load_dotenv(dotenv_path=dotenv_path)

# Get API keys from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVEN_LABS_API_KEY = os.getenv("ELEVEN_LABS_API_KEY")

# Initialize APIs
client = OpenAI(api_key=OPENAI_API_KEY)
eleven_labs = ElevenLabs(api_key=ELEVEN_LABS_API_KEY)

# Use voice names instead of IDs
VOICE_1 = "George"
VOICE_2 = "Matilda"

# Create an 'audio_files' directory if it doesn't exist
AUDIO_DIR = "audio_files"
if not os.path.exists(AUDIO_DIR):
    os.makedirs(AUDIO_DIR)


def generate_conversation(topic, num_exchanges=3):
    """Generate a conversation using OpenAI."""
    prompt = f"""
    Create a natural podcast conversation between two hosts about {topic}.
    The conversation should have {num_exchanges} exchanges. 
    Format the output as alternating lines starting with "Host1:" or "Host2:".
    Make it sound casual and engaging, with each host building on what the other says.
    
    Conversation:
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are helping create a podcast conversation between two hosts. Add in some playful banter and interesting insights to keep the conversation engaging.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
    )

    return response.choices[0].message.content.strip().split("\n")


def text_to_speech(text, voice_name, filename):
    """Convert text to speech using ElevenLabs API and save locally."""
    try:
        # Generate audio using voice name instead of ID
        audio = eleven_labs.generate(
            text=text, voice=voice_name, model="eleven_multilingual_v2"
        )

        # Collect all chunks into a single bytes object
        audio_data = b""
        for chunk in audio:
            audio_data += chunk

        # Create full path for the file
        filepath = os.path.join(AUDIO_DIR, filename)

        # Save the audio to a file
        with open(filepath, "wb") as f:
            f.write(audio_data)

        print(f"Audio saved to: {filepath}")
        return filepath
    except Exception as e:
        print(f"Error in text_to_speech: {str(e)}")
        raise


def combine_audio_files(audio_files, output_filename):
    """Combine multiple audio files with a small pause between them."""
    combined = AudioSegment.empty()
    pause = AudioSegment.silent(duration=500)  # 500ms pause

    for audio_file in audio_files:
        segment = AudioSegment.from_mp3(audio_file)
        combined += segment + pause

    # Save final output to audio_files directory
    output_path = os.path.join(AUDIO_DIR, output_filename)
    combined.export(output_path, format="mp3")
    return output_path


def create_podcast(topic, output_filename, num_exchanges=3):
    """Create a complete podcast episode."""
    try:
        # Generate conversation
        print("Generating conversation...")
        conversation_lines = generate_conversation(topic, num_exchanges)

        # Create temporary audio files
        audio_files = []
        for i, line in enumerate(conversation_lines):
            if line.strip():
                try:
                    speaker, text = line.split(":", 1)
                    voice = VOICE_1 if speaker.strip() == "Host1" else VOICE_2
                    temp_filename = f"segment_{i}.mp3"

                    print(f"Generating audio for {speaker} using voice {voice}...")
                    filepath = text_to_speech(text.strip(), voice, temp_filename)
                    audio_files.append(filepath)
                except ValueError as e:
                    print(f"Skipping invalid line: {line}")
                    continue

        # Combine all audio files
        print("Combining audio files...")
        final_path = combine_audio_files(audio_files, output_filename)

        # Clean up individual segment files
        for file in audio_files:
            os.remove(file)
            print(f"Cleaned up temporary file: {file}")

        print(f"Podcast created successfully at: {final_path}")

    except Exception as e:
        print(f"Error creating podcast: {str(e)}")


if __name__ == "__main__":
    topic = "The future of artificial intelligence and its impact on society"
    output_filename = "ai_podcast_episode.mp3"
    create_podcast(topic, output_filename, num_exchanges=3)
