# Installation

## Requirements

- Python 3.8 or higher
- Mathpix CLI (`mpx`) for PDF to markdown conversion
- Anki with AnkiConnect addon (for Anki integration)
- API keys for OpenAI and ElevenLabs (for AI features)

## Install from PyPI

```bash
pip install swanki
```

## Install from Source

```bash
git clone https://github.com/yourusername/swanki.git
cd swanki
pip install -e .
```

## Setting up Mathpix

1. Sign up for a Mathpix account at [https://mathpix.com/](https://mathpix.com/)
2. Install the Mathpix CLI:
   ```bash
   npm install -g @mathpix/mpx-cli
   ```
3. Authenticate:
   ```bash
   mpx login
   ```

## Setting up API Keys

Create a `.env` file in your project directory:

```bash
OPENAI_API_KEY=your_openai_api_key_here
ELEVEN_LABS_API_KEY=your_elevenlabs_api_key_here
```

## Installing AnkiConnect

1. Open Anki
2. Go to Tools → Add-ons → Get Add-ons
3. Enter code: `2055492159`
4. Restart Anki

## Verify Installation

```bash
swanki --help
```