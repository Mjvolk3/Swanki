"""Configuration generator for Swanki's Hydra-based config system.

This module provides the ConfigGenerator class which automatically creates
default configuration files for the Swanki pipeline. It generates a complete
set of Hydra configs covering all aspects of the processing pipeline.

Classes
-------
ConfigGenerator
    Auto-generates default Hydra configs if not present

Examples
--------
>>> from swanki.config import ConfigGenerator
>>> 
>>> # Ensure configs exist (called automatically by CLI)
>>> config_dir = ConfigGenerator.ensure_configs()
>>> print(f"Configs available at: {config_dir}")
Configs available at: /path/to/project/.swanki_config

Notes
-----
Configuration structure:
- Main config.yaml with defaults list
- Subdirectories for each config group:
  - pipeline/: Processing settings
  - prompts/: AI prompt templates  
  - models/: LLM and TTS settings
  - audio/: Audio generation options
  - output/: Output format settings
  - anki/: Anki integration settings
"""

from pathlib import Path
import yaml
from typing import Dict, Any


class ConfigGenerator:
    """Auto-generates default Hydra configs if not present.
    
    Creates a complete configuration structure for Swanki with sensible
    defaults. Configs are created in a .swanki_config directory in the
    current working directory.
    
    Attributes
    ----------
    DEFAULT_CONFIG_DIR : Path
        Default directory name for configs (.swanki_config)
    
    Methods
    -------
    ensure_configs()
        Ensure config directory exists with all defaults
    
    Examples
    --------
    >>> # Automatically called by CLI
    >>> config_dir = ConfigGenerator.ensure_configs()
    >>> 
    >>> # Configs are now available for Hydra
    >>> # Users can override by editing files in .swanki_config/
    """
    
    DEFAULT_CONFIG_DIR = Path(".swanki_config")
    
    @classmethod
    def ensure_configs(cls, interactive: bool = True) -> Path:
        """Ensure config directory exists with all defaults.
        
        Creates the configuration directory and generates all default
        configuration files if they don't already exist. Called automatically
        by the CLI before Hydra initialization.
        
        Parameters
        ----------
        interactive : bool, optional
            Whether to prompt user when creating configs (default is True)
        
        Returns
        -------
        Path
            Path to the configuration directory
        
        Notes
        -----
        - Only creates configs if directory doesn't exist
        - Won't overwrite existing user modifications
        - Creates in current working directory
        """
        config_dir = Path.cwd() / cls.DEFAULT_CONFIG_DIR
        
        if not config_dir.exists():
            print(f"\n{'='*60}")
            print("FIRST TIME SETUP: No configuration found")
            print(f"{'='*60}")
            print(f"\nSwanki will create default configuration files at:")
            print(f"  {config_dir}")
            print("\nThese configs control:")
            print("  - Number of cards generated per page")
            print("  - Audio generation settings (speed, voice)")
            print("  - LLM model selection")
            print("  - Anki integration options")
            print("  - Output formats and organization")
            
            if interactive:
                print(f"\n{'='*60}")
                response = input("\nCreate configs with defaults? [Y/n]: ").strip().lower()
                
                if response and response not in ['y', 'yes', '']:
                    print("\nConfiguration cancelled. You can manually create configs at:")
                    print(f"  {config_dir}")
                    print("\nOr run the command again to use defaults.")
                    import sys
                    sys.exit(0)
            
            print(f"\nCreating default configurations...")
            config_dir.mkdir(parents=True, exist_ok=True)
            cls._generate_all_defaults(config_dir)
            
            print(f"\n✓ Configurations created! Processing will continue with defaults.")
            print(f"\nTo customize settings, edit files in: {config_dir}/")
            print(f"Key files: pipeline/default.yaml, prompts/default.yaml, audio/default.yaml")
            
            # No second prompt - just continue
            print(f"\n{'='*60}\n")
        
        return config_dir
    
    @classmethod
    def _generate_all_defaults(cls, config_dir: Path):
        """Generate all default configuration files.
        
        Creates the complete configuration structure with all config
        groups and their variants.
        
        Parameters
        ----------
        config_dir : Path
            Root configuration directory
        
        Notes
        -----
        Config groups created:
        - pipeline: Processing parameters (default, comprehensive, fast)
        - prompts: AI prompts (default, technical)
        - models: LLM/TTS settings (default, openai_tts)
        - audio: Audio generation (default, cards, summary, reading, full)
        - output: Output formats (default)
        - anki: Anki integration (default, auto_send, custom_deck)
        """
        
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
                "cloze_cards_per_page": 2,  # Number of cloze deletion cards per page
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
                "cloze_cards_per_page": 3,  # More cloze cards for comprehensive mode
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
                "cloze_cards_per_page": 1,  # Fewer cloze cards for fast mode
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
                    "image_summary": """Provide a comprehensive description of this image for audio-only learners.

Instructions:
1. Describe the overall structure and layout of the image (4-6 sentences)
2. Detail all key components, labels, and relationships shown
3. If it contains equations, describe them precisely using natural language
4. If it shows a process or flow, describe the sequence and connections
5. Include any text labels, annotations, or legends
6. Describe visual elements that convey meaning (arrows, colors, shapes)
7. DO NOT interpret or explain what the image means - just describe what is shown

The description should be detailed enough that someone listening to audio only can understand:
- What type of visual it is (graph, diagram, flowchart, etc.)
- What elements are present and how they're arranged
- What relationships or processes are depicted
- Any mathematical or technical notation shown

Aim for 6-10 sentences that paint a complete picture without revealing answers to potential questions."""
                },
                "cards": {
                    "system": "You are an expert at creating educational flashcards. Your ONLY job is to create the EXACT number of cards requested. You MUST create BOTH regular Q&A cards AND cloze deletion cards as specified. Count carefully and ensure you generate the exact numbers requested.",
                    "generate_cards": """You are required to generate {num_cards} regular cards AND {num_cloze} cloze deletion cards.

MANDATORY DISTRIBUTION:
- Regular Q&A cards: {num_cards}
- Cloze deletion cards: {num_cloze}
- Total cards to generate: {num_cards} + {num_cloze}

Context from document summary:
Title: {title}
Acronyms: {acronyms}
Technical terms: {technical_terms}

Content:
{content}

CRITICAL RULE: CARDS MUST BE SELF-CONTAINED
Every card must contain ALL information needed to understand and answer it. Students will NOT have access to:
- The original paper or document
- Other papers or references
- Figures, tables, or diagrams (unless embedded in the card)
- Previous or subsequent cards
- Any external context

FORBIDDEN CONTENT - NEVER CREATE CARDS WITH:
- References to other papers: "According to Smith et al. [12]..." or "As shown in reference [7]..."
- ANY reference numbers: "ref. [6]", "[1]", "(Smith, 2023)", "the framework in [6]", "reference ${ }^{6}$", "${ }^{12}$", "{ }^{7}"
- Figure/table references: "Figure 3 shows..." or "As seen in Table 2..."
- Context-dependent phrases: "The above equation...", "This method...", "The aforementioned..."
- Vague referents: "this framework", "the model", "this approach" (without explaining WHAT framework/model/approach)
- Document references: "in the context of the document", "as described in the document", "the document states"
- LaTeX tables (\\\\begin{{tabular}}) - they don't render properly in Anki
- External citations that students can't access
- Author-focused questions: "How does Lachapelle et al. approach...", "What is Zheng et al.'s method..."
- Simple acronym expansions: "What does SEM stand for?" (instead ask about what SEM IS or HOW it works)

CRITICAL: If the content mentions "ref. [X]" or "framework in [Y]", you MUST:
1. Extract the actual innovation/method being described
2. Describe it directly without the reference number
3. Make the card about the concept itself, not about who proposed it

EXAMPLE TRANSFORMATIONS:
❌ BAD: "What innovation did the framework in ref. [6] introduce?"
✓ GOOD: "What innovation transformed discrete DAG optimization into continuous optimization?"

❌ BAD: "According to [12], what is the complexity of the algorithm?"
✓ GOOD: "What is the time complexity of learning Bayesian network structures?"

❌ BAD: "How does the method in ref. [8] differ from previous approaches?"
✓ GOOD: "How does continuous optimization for DAG learning differ from combinatorial approaches?"

BAD EXAMPLES TO AVOID:
❌ "What transformation is applied in this framework?" (WHAT framework?)
❌ "How does the model handle missing data?" (WHAT model?)
❌ "What is the advantage of this approach?" (WHAT approach?)
❌ "In the context of the document, what does h(W) = 0 represent?" (Remove "in the context of the document")
❌ "What innovation did the framework described in reference ${ }^{6}$ bring?" (Remove reference number)
❌ "Describe how Lachapelle et al. approach causal inference" (Focus on the method, not the authors)
❌ "What does NAS stand for?" (Simple memorization - ask what NAS DOES instead)

GOOD EXAMPLES:
✓ "What transformation is applied in the causal inference framework that combines DAGs with deep learning?"
✓ "How does the multi-layer perceptron model handle missing data in the feature matrix?"
✓ "What is the advantage of combining causal inference with deep learning for dimensionality reduction?"

CLOZE DELETION CARD FORMAT (YOU MUST CREATE {num_cloze} OF THESE):
## [Self-contained statement with {{c1::hidden text}} that tests understanding]

- #tag1, #tag2

CRITICAL: Every cloze card MUST have tags on the "- #tag1, #tag2" line just like regular cards!

IMPORTANT CLOZE RULES:
- Hide meaningful concepts, definitions, or key terms
- For equations: You can hide PARTS of simple equations OR entire complex equations
- CRITICAL: When mentioning an equation, the ENTIRE equation must be inside cloze markers
- Make cards educational - test understanding, not memorization
- Each card must stand alone without external context

CRITICAL MATH CLOZE RULES:
- If you mention "the equation" followed by math, the ENTIRE equation goes inside {{c1::...}}
- NEVER write: "The equation {{c1::something}} \\(actual equation\\)"
- CORRECT: "The equation {{c1::\\(E[X_j | X_{pa(j)}] = g_j(f_j(X))\\)}} expresses..."
- For simple equations, you can hide parts: "The derivative \\(\\frac{d}{dx}(x^2) = {{c1::2x}}\\)"

Example GOOD cloze cards:
## The gradient of \\(f(x) = x^2\\) is {{c1::2x}}, which represents the {{c2::rate of change}}.

- #calculus.derivatives, #mathematics

## In Bayesian networks, conditional dependencies are represented by {{c1::directed edges}} in a {{c2::directed acyclic graph (DAG)}}.

- #bayesian-networks, #graphical-models

## The equation {{c1::\\(E[X_j \\mid X_{pa(j)}] = g_j(f_j(X))\\)}} expresses the {{c2::conditional expectation of a node given its parents}}.

- #statistics, #conditional-expectation

## In causal modeling, conditional dependencies are expressed using {{c1::\\(\\sum_{i=1}^{n} w_{ij}x_i + b_j\\)}} as the {{c2::structural equation}}.

- #causal-inference, #structural-equations

## The transformation {{c1::\\(F(W)\\)}} maps {{c2::weighted adjacency matrices}} to {{c3::directed acyclic graphs}}.

- #graph-theory, #transformations, #dag-learning

Example BAD cloze cards to AVOID:
- "According to [12], the algorithm is {{c1::efficient}}" (References external paper)
- "The original constraints are replaced by {{c1::continuous equality}}" (What original constraints?)
- "As shown in Figure 3, performance {{c1::improves}}" (No access to Figure 3)
- "The equation {{c1::describes relationships}} \\(E[X | Y] = f(Y)\\)" (Equation is outside cloze!)
- "Using equation {{c1::MathJax}} to express dependencies" (Meaningless placeholder)

REGULAR Q&A CARD FORMAT (YOU MUST CREATE {num_cards} OF THESE):
## [Self-contained question that provides all necessary context]

[Complete answer that doesn't reference external content]

- #tag1, #tag2

Example GOOD regular cards:
## What is the time complexity of quicksort in the average case?

The average case time complexity of quicksort is O(n log n), where n is the number of elements to sort. This assumes random pivot selection and balanced partitions.

- #algorithms.sorting, #complexity-analysis

## How does gradient descent minimize a loss function?

Gradient descent iteratively updates parameters by moving in the direction opposite to the gradient. At each step, it computes the gradient of the loss function and updates parameters: θ = θ - α∇L(θ), where α is the learning rate.

- #optimization, #machine-learning.algorithms

Example BAD regular cards to AVOID:
## According to the paper, what is the main contribution?

(Bad - which paper? Students don't have access to it)

## What does Table 3 show about performance?

(Bad - students can't see Table 3)

## In the context of the document, what does the equation $h(W) = 0$ represent?

(Bad - "in the context of the document" is vague, and h is undefined)

## What is the significance of Zheng et al.'s nonparametric model in DAG learning?

(Bad - asks about specific authors instead of the concept)

## What does SEM stand for, and how is it used in this context?

(Bad - "What does X stand for" is rote memorization, and "in this context" is vague)

## What approach does Lachapelle et al. use for causal inference?

(Bad - focuses on authors rather than the method itself)

CRITICAL REQUIREMENTS:
1. YOU MUST generate EXACTLY {num_cloze} cloze deletion cards (with {{c1::...}} syntax)
2. YOU MUST generate EXACTLY {num_cards} regular Q&A cards
3. EVERY card MUST be completely self-contained - no external references
4. EVERY card MUST have AT LEAST 2 meaningful tags on the "- #tag1, #tag2" line
5. Tags should be hierarchical when appropriate (e.g., #algorithms.sorting, #optimization.gradient-based)
6. Never start the question with the citation - it will be added automatically
7. PRIORITIZE creating cards about:
   - Mathematical equations, formulas, and their meanings
   - Algorithm steps, complexity, and implementation details  
   - Proofs, derivations, and mathematical relationships
   - Statistical methods and their applications
   - Computational techniques and optimizations
   - ANY mathematical notation present in the content (e.g., \\(F(W)\\), \\(I - W^T\\), etc.)
8. Use MathJax format: \\(...\\) for inline math, \\[...\\] for display math
9. NEVER use $ or $$ delimiters - Anki uses \\( \\) and \\[ \\]
10. NEVER use LaTeX tables (\\\\begin{{tabular}})
11. For cloze cards with math: If }} appears in your LaTeX, add a space before it
    Example: {{c1::The formula \\(\\frac{a}{\\frac{b}{c} }\\) shows...}} (note the space before })
12. For cloze cards with :: in content: Use HTML comment
    Example: {{c1::std:<!-- -->:variant is a C++ feature}}
13. For equation cloze cards: When referencing "the equation", include the ENTIRE equation in cloze
    Example: "The equation {{c1::\\(E = mc^2\\)}} demonstrates..." NOT "The equation {{c1::E=mc²}} \\(E = mc^2\\)..."
14. Each card must teach a concept, not test memorization of references
15. IMPORTANT: When you find ANY mathematical notation, CREATE CARDS about it!
16. NEVER use generic tags like #equation, #formula, #definition, #concept, #method
    Use specific conceptual tags: #optimization.gradient-descent, #causal-inference.dag, #machine-learning.regularization
17. ALWAYS define mathematical symbols within the card: "where h is a smooth function" not just "h(W) = 0"
18. ALWAYS expand acronyms when first used: "NAS (Neural Architecture Search)" not just "NAS"
19. For EVERY mathematical symbol or function (h, F, g_j, etc.), ensure the card defines what it represents
20. Focus on WHAT methods do and HOW they work, not WHO proposed them
21. Transform author-centric questions into concept-centric ones:
    ❌ "What is Zheng et al.'s approach?" 
    ✓ "How does the nonparametric DAG learning method work?"

Start generating cards now. First generate all {num_cloze} cloze cards, then generate all {num_cards} regular cards."""
                },
                "audio": {
                    "transcript_cleaning": """Convert this text to be TTS-friendly:
1. Expand acronyms on first use
2. Convert math notation to words
3. Add pronunciation guides for technical terms
4. Ensure citation key is read at start of card

Text: {text}
Citation key: {citation_key}
Known acronyms: {acronyms}""",
                    "lecture_system": """You are creating a clear, informative audio presentation of academic content.
Focus on clarity and educational value without unnecessary dramatization.
Start directly with the content without lengthy introductions.""",
                    "lecture_generation": """Create a clear educational presentation from this document.

Guidelines:
1. Begin directly with the main content - no lengthy introductions
2. Use a professional, informative tone
3. Focus on key concepts and findings
4. Avoid theatrical or overly dramatic language
5. End concisely without extended conclusions
6. Mention the citation key naturally at the beginning: {citation_key}

Content to present:
{content}"""
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
                "deck_name": "{deck_name}",  # Uses output_dir if specified, otherwise citation_key
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
                "deck_name": "{deck_name}",  # Uses output_dir if specified, otherwise citation_key
                "card_format": "with_audio"
            }
        })
        
        cls._write_yaml(anki_dir / "custom_deck.yaml", {
            "anki": {
                "enabled": True,
                "deck_name": "Research::Papers::{deck_name}",  # Custom hierarchy with output_dir or citation_key
                "auto_send": False
            }
        })
    
    @staticmethod
    def _write_yaml(path: Path, data: Dict[str, Any]):
        """Write YAML file with nice formatting.
        
        Parameters
        ----------
        path : Path
            Output file path
        data : Dict[str, Any]
            Configuration data to write
        
        Notes
        -----
        - Uses default_flow_style=False for readable output
        - Preserves key order with sort_keys=False
        """
        with open(path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)