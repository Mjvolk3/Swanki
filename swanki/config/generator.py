from pathlib import Path
import yaml
from typing import Dict, Any


class ConfigGenerator:
    """Auto-generates default Hydra configs if not present"""
    
    DEFAULT_CONFIG_DIR = Path(".swanki_config")
    
    @classmethod
    def ensure_configs(cls) -> Path:
        """Ensure config directory exists with all defaults"""
        config_dir = Path.cwd() / cls.DEFAULT_CONFIG_DIR
        
        if not config_dir.exists():
            print(f"Creating default configs at {config_dir}")
            config_dir.mkdir(parents=True, exist_ok=True)
            cls._generate_all_defaults(config_dir)
        
        return config_dir
    
    @classmethod
    def _generate_all_defaults(cls, config_dir: Path):
        """Generate all default configuration files"""
        
        # Main config
        cls._write_yaml(config_dir / "config.yaml", {
            "defaults": [
                "_self_",
                {"pipeline": "default"},
                {"prompts": "default"}, 
                {"models": "default"},
                {"audio": "default"},
                {"output": "default"},
                {"anki": "default"}
            ],
            "pdf_path": None,  # Will be provided by user
            "citation_key": None,  # Will be provided by user
            # Add placeholder keys so Hydra knows about them
            "pipeline": None,  # Will be overridden by defaults
            "prompts": None,   # Will be overridden by defaults
            "models": None,    # Will be overridden by defaults
            "audio": None,     # Will be overridden by defaults
            "output": None,    # Will be overridden by defaults
            "anki": None,      # Will be overridden by defaults
            "hydra": {
                "run": {
                    "dir": "outputs/${now:%Y-%m-%d}/${now:%H-%M-%S}"
                }
            }
        })
        
        # Pipeline configs
        pipeline_dir = config_dir / "pipeline"
        pipeline_dir.mkdir(exist_ok=True)
        
        cls._write_yaml(pipeline_dir / "default.yaml", {
            "processing": {
                "window_size": 2,
                "skip": 1,
                "num_cards_per_page": 3,
                "chunk_size": 1000,
                "overlap": 200,
                "blocking_audio": True,  # Based on learnings
                "image_cards": {
                    "enabled": True,
                    "cards_per_image": 3,
                    "image_on_front": True,  # Whether image can appear on front of card
                    "image_on_back": True,   # Whether image can appear on back of card
                    "require_math_content": False,  # Only create cards for images with math
                    "placement_strategy": "smart",  # How to decide placement when both front/back are true
                    # "smart": Based on question content (if it references the image)
                    # "alternate": Alternate between front and back
                    # "random": Random placement with front_back_ratio
                    # "prefer_front": Always front when possible
                    # "prefer_back": Always back when possible
                    "front_back_ratio": 0.5  # For random strategy: probability of front placement (0.0-1.0)
                }
            }
        })
        
        cls._write_yaml(pipeline_dir / "comprehensive.yaml", {
            "processing": {
                "window_size": 3,
                "skip": 1,
                "num_cards_per_page": 5,
                "chunk_size": 1500,
                "overlap": 300,
                "blocking_audio": True
            }
        })
        
        cls._write_yaml(pipeline_dir / "fast.yaml", {
            "processing": {
                "window_size": 1,
                "skip": 1,
                "num_cards_per_page": 2,
                "chunk_size": 800,
                "overlap": 100,
                "blocking_audio": False
            }
        })
        
        # Prompts configs
        prompts_dir = config_dir / "prompts"
        prompts_dir.mkdir(exist_ok=True)
        
        cls._write_yaml(prompts_dir / "default.yaml", {
            "prompts": {
                "summary": {
                    "system": "You are an expert at creating concise, informative summaries of academic documents.",
                    "document_summary": """Create a comprehensive summary of this document.
Focus on:
1. Main thesis and key contributions
2. All acronyms and their full forms
3. Technical terms that need clear definitions
4. Methodology and approach
5. Key findings

Document content:
{content}

Image summaries:
{image_summaries}""",
                    "image_summary": """Describe this image in 2-3 sentences.
Focus on what information it conveys and its relevance.
If it contains equations or data, describe them clearly."""
                },
                "cards": {
                    "system": "You are an expert at creating educational flashcards in VSCode Anki format that test understanding.",
                    "generate_cards": """Create {num_cards} flashcards from this content in VSCode Anki format.

Context from document summary:
Title: {title}
Acronyms: {acronyms}
Technical terms: {technical_terms}

Content:
{content}

FORMAT RULES:
1. Use ## for the question (front of card)
2. Answer goes on the next line (back of card)
3. Tags go as a single bullet: - #tag1, #tag2, #tag3
4. Use period-delimited tags from broad to narrow (e.g., #biology.cell-biology, #chemistry.organic)

CONTENT RULES:
1. Each card tests ONE concept
2. Use full forms of acronyms in answers
3. Include necessary context in questions
4. Answers should be comprehensive but concise
5. Use LaTeX with $ for inline and $$ for display math

Example card:
## What is the role of ATP in cellular metabolism?

ATP (Adenosine Triphosphate) serves as the primary energy currency of cells. It stores energy in its high-energy phosphate bonds and releases it when hydrolyzed to ADP, powering various cellular processes including active transport, muscle contraction, and biosynthesis.

- #biology.cellular-metabolism, #biochemistry.energy-metabolism"""
                },
                "audio": {
                    "transcript_cleaning": """Convert this text to be TTS-friendly:
1. Expand acronyms on first use
2. Convert math notation to words
3. Add pronunciation guides for technical terms
4. Ensure citation key is read at start of card

Text: {text}
Citation key: {citation_key}
Known acronyms: {acronyms}"""
                }
            }
        })
        
        cls._write_yaml(prompts_dir / "technical.yaml", {
            "prompts": {
                "summary": {
                    "system": "You are an expert in technical and scientific literature.",
                    "document_summary": """Create a technical summary focusing on:
1. Mathematical formulations
2. Algorithm descriptions
3. Technical acronyms and notation
4. Implementation details
5. Experimental setup

{content}"""
                }
            }
        })
        
        # Models configs
        models_dir = config_dir / "models"
        models_dir.mkdir(exist_ok=True)
        
        cls._write_yaml(models_dir / "default.yaml", {
            "models": {
                "llm": {
                    "provider": "openai",
                    "model": "gpt-4o",
                    "temperature": 0.7,
                    "max_retries": 3
                },
                "tts": {
                    "provider": "elevenlabs",
                    "voice_id": "21m00Tcm4TlvDq8ikWAM",  # Rachel
                    "model": "eleven_monolingual_v1",
                    "stability": 0.5,
                    "similarity_boost": 0.5
                }
            }
        })
        
        cls._write_yaml(models_dir / "openai_tts.yaml", {
            "models": {
                "tts": {
                    "provider": "openai",
                    "voice": "nova",
                    "model": "tts-1-hd",
                    "speed": 1.0
                }
            }
        })
        
        # Audio configs
        audio_dir = config_dir / "audio"
        audio_dir.mkdir(exist_ok=True)
        
        cls._write_yaml(audio_dir / "default.yaml", {
            "audio": {
                "generate_complementary": False,
                "generate_summary": False,
                "generate_reading": False,
                "complementary_speed": 1.6,
                "summary_speed": 1.1,
                "reading_speed": 1.2,
                "format": "mp3",
                "quality": "high"
            }
        })
        
        # Only card audio
        cls._write_yaml(audio_dir / "cards.yaml", {
            "audio": {
                "generate_complementary": True,
                "generate_summary": False,
                "generate_reading": False,
                "complementary_speed": 1.6
            }
        })
        
        # Only summary audio
        cls._write_yaml(audio_dir / "summary.yaml", {
            "audio": {
                "generate_complementary": False,
                "generate_summary": True,
                "generate_reading": False,
                "summary_speed": 1.1
            }
        })
        
        # Only reading audio
        cls._write_yaml(audio_dir / "reading.yaml", {
            "audio": {
                "generate_complementary": False,
                "generate_summary": False,
                "generate_reading": True,
                "reading_speed": 1.2
            }
        })
        
        # All audio types
        cls._write_yaml(audio_dir / "full.yaml", {
            "audio": {
                "generate_complementary": True,
                "generate_summary": True,
                "generate_reading": True,
                "complementary_speed": 1.6,
                "summary_speed": 1.1,
                "reading_speed": 1.2
            }
        })
        
        # Output configs
        output_dir = config_dir / "output"
        output_dir.mkdir(exist_ok=True)
        
        cls._write_yaml(output_dir / "default.yaml", {
            "output": {
                "base_dir": "swanki-out",
                "formats": {
                    "cards_plain": "cards-plain.md",
                    "cards_audio": "cards-with-audio.md",
                    "cards_combined": "cards-combined.md",
                    "summary": "document-summary.md"
                },
                "organize_by_type": True,
                "create_anki_deck": False,
                "tag_format": "slugified"  # Options: "slugified", "spaces", "raw"
            }
        })
        
        # Anki configs
        anki_dir = config_dir / "anki"
        anki_dir.mkdir(exist_ok=True)
        
        cls._write_yaml(anki_dir / "default.yaml", {
            "anki": {
                "enabled": False,
                "deck_name": "{citation_key}",  # Template variable support
                "host": "127.0.0.1",
                "port": 8765,
                "auto_send": False,  # Whether to automatically send cards after generation
                "update_existing": True,  # Whether to update existing cards
                "media_upload": True,  # Whether to upload media files (images, audio)
                "card_format": "with_audio"  # Options: "plain", "with_audio"
            }
        })
        
        cls._write_yaml(anki_dir / "auto_send.yaml", {
            "anki": {
                "enabled": True,
                "auto_send": True,
                "deck_name": "{citation_key}",
                "card_format": "with_audio"
            }
        })
        
        cls._write_yaml(anki_dir / "custom_deck.yaml", {
            "anki": {
                "enabled": True,
                "deck_name": "Research::Papers::{citation_key}",  # Custom hierarchy
                "auto_send": False
            }
        })
    
    @staticmethod
    def _write_yaml(path: Path, data: Dict[str, Any]):
        """Write YAML file with nice formatting"""
        with open(path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)