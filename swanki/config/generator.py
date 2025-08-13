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
                response = (
                    input("\nCreate configs with defaults? [Y/n]: ").strip().lower()
                )

                if response and response not in ["y", "yes", ""]:
                    print(
                        "\nConfiguration cancelled. You can manually create configs at:"
                    )
                    print(f"  {config_dir}")
                    print("\nOr run the command again to use defaults.")
                    import sys

                    sys.exit(0)

            print(f"\nCreating default configurations...")
            config_dir.mkdir(parents=True, exist_ok=True)
            cls._generate_all_defaults(config_dir)

            print(f"\n✓ Configurations created!")
            print(f"\nTo customize settings, edit files in: {config_dir}/")
            print(
                f"Key files: pipeline/default.yaml, prompts/default.yaml, audio/default.yaml"
            )

            # Add second prompt to allow user to halt and edit configs
            if interactive:
                print(f"\n{'='*60}")
                print("\nWould you like to:")
                print("  1. Continue processing with default settings")
                print("  2. Halt to edit configuration files first")
                print(f"{'='*60}")

                response = input("\nContinue with defaults? [Y/n]: ").strip().lower()

                if response and response not in ["y", "yes", ""]:
                    print(
                        "\nProcessing halted. You can now edit the configuration files at:"
                    )
                    print(f"  {config_dir}/")
                    print(
                        "\nOnce you've customized the settings, run the command again."
                    )
                    print("The configuration files will be used automatically.")
                    import sys

                    sys.exit(0)

                print(f"\nContinuing with default settings...")

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
        cls._write_yaml(
            config_dir / "config.yaml",
            {
                "defaults": [
                    "_self_",
                    {"pipeline": "default"},
                    {"prompts": "default"},
                    {"models": "default"},
                    {"audio": "default"},
                    {"output": "default"},
                    {"anki": "default"},
                    {"refinement": "default"},
                ],
                "pdf_path": None,  # Will be provided by user
                "citation_key": None,  # Will be provided by user
                # Add placeholder keys so Hydra knows about them
                "pipeline": None,  # Will be overridden by defaults
                "prompts": None,  # Will be overridden by defaults
                "models": None,  # Will be overridden by defaults
                "audio": None,  # Will be overridden by defaults
                "output": None,  # Will be overridden by defaults
                "anki": None,  # Will be overridden by defaults
                "refinement": None,  # Will be overridden by defaults
                "hydra": {"run": {"dir": "outputs/${now:%Y-%m-%d}/${now:%H-%M-%S}"}},
            },
        )

        # Pipeline configs
        pipeline_dir = config_dir / "pipeline"
        pipeline_dir.mkdir(exist_ok=True)

        cls._write_yaml(
            pipeline_dir / "default.yaml",
            {
                "processing": {
                    "context_radius": 1,  # Number of pages before/after focal page for context (0 = no context)
                    "num_cards_per_page": 4,  # Updated default from 3
                    "cloze_cards_per_page": 1,  # Updated default from 2
                    "chunk_size": 1000,
                    "overlap": 200,
                    "blocking_audio": True,  # Based on learnings
                    "confirm_before_generation": True,  # Ask user confirmation after card estimation
                    "image_cards": {
                        "enabled": True,
                        "cards_per_image": 3,
                        "image_on_front": True,  # Whether image can appear on front of card
                        "image_on_back": True,  # Whether image can appear on back of card
                        "require_math_content": False,  # Only create cards for images with math
                        "placement_strategy": "prefer_front",  # How to decide placement when both front/back are true
                        # "smart": Based on question content (if it references the image)
                        # "alternate": Alternate between front and back
                        # "random": Random placement with front_back_ratio
                        # "prefer_front": Always front when possible
                        # "prefer_back": Always back when possible
                        "front_back_ratio": 0.5,  # For random strategy: probability of front placement (0.0-1.0)
                    },
                }
            },
        )

        cls._write_yaml(
            pipeline_dir / "standard.yaml",
            {
                "processing": {
                    "context_radius": 1,  # Standard context window
                    "num_cards_per_page": 4,
                    "cloze_cards_per_page": 1,  # Standard cloze count
                    "chunk_size": 1000,
                    "overlap": 200,
                    "blocking_audio": True,
                    "confirm_before_generation": True,
                }
            },
        )

        cls._write_yaml(
            pipeline_dir / "larger.yaml",
            {
                "processing": {
                    "context_radius": 2,  # Larger context for more cards
                    "num_cards_per_page": 5,
                    "cloze_cards_per_page": 3,  # More cloze cards
                    "chunk_size": 1500,
                    "overlap": 300,
                    "blocking_audio": True,
                    "confirm_before_generation": True,
                }
            },
        )

        cls._write_yaml(
            pipeline_dir / "smaller.yaml",
            {
                "processing": {
                    "context_radius": 0,  # No context for fewer cards
                    "num_cards_per_page": 2,
                    "cloze_cards_per_page": 1,  # Minimal cloze cards
                    "chunk_size": 800,
                    "overlap": 100,
                    "blocking_audio": False,
                    "confirm_before_generation": False,  # Skip confirmation
                }
            },
        )

        # Prompts configs
        prompts_dir = config_dir / "prompts"
        prompts_dir.mkdir(exist_ok=True)

        cls._write_yaml(
            prompts_dir / "default.yaml",
            {
                "prompts": {
                    "summary": {
                        "system": "You are an expert educator creating lecture-style summaries that help students deeply understand academic material. Your summaries should be comprehensive, engaging, and educational.",
                        "document_summary": """Create a comprehensive lecture-style summary that an eager student would use to understand this material deeply.

Structure your summary as follows:

1. **Introduction and Motivation** (why this matters)
   - Context and background
   - Why students should care about this topic
   - Connection to broader fields

2. **Core Concepts and Definitions**
   - All key terms explained clearly
   - Intuitive explanations before formal definitions
   - Relationships between concepts

3. **Key Mathematical Formulations** (with intuitive explanations)
   - Important equations with explanations of what they mean
   - Variable definitions and significance
   - Physical or conceptual interpretations

4. **Methodology and Techniques**
   - Step-by-step explanation of approaches
   - Why these methods were chosen
   - Strengths and limitations

5. **Main Results and Their Significance**
   - Key findings explained clearly
   - What these results mean in practice
   - Impact on the field

6. **Practical Applications and Examples**
   - Real-world uses
   - Concrete examples to illustrate concepts
   - How students might apply this knowledge

7. **Connections to Broader Topics**
   - How this relates to other areas
   - Future directions
   - Open questions

Additional requirements:
- Include ALL important equations with explanations of what they mean intuitively
- Define ALL technical terms and acronyms clearly (provide a comprehensive list)
- Explain the "why" behind concepts, not just the "what"
- Use analogies and examples to clarify complex ideas
- Write as if preparing students for deep understanding, not memorization
- Highlight conceptual insights and "aha" moments

Target length: 
- For short documents (1-5 pages): 100-500 words
- For medium documents (6-20 pages): 300-800 words  
- For long documents (20+ pages): 500-1500 words
Be comprehensive and educational while being appropriate to document length.

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

Aim for 6-10 sentences that paint a complete picture without revealing answers to potential questions.""",
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

CRITICAL RULES FOR SELF-CONTAINED CARDS:
1. Every card must contain ALL information needed to understand and answer it
2. If an equation is part of a larger example, PROVIDE THE CONTEXT
3. If values or parameters are mentioned, SPECIFY WHAT THEY ARE
4. If comparing quantities, PROVIDE THE BASELINE FOR COMPARISON
5. Always include enough background to make the card meaningful

Students will NOT have access to:
- The original paper or document
- Other papers or references
- Figures, tables, or diagrams (unless embedded in the card)
- Previous or subsequent cards
- Any external context

EDUCATIONAL VALUE REQUIREMENTS:
- Focus on KEY CONCEPTS that matter for understanding the subject
- Avoid trivial questions about notation or random equation parameters
- Prioritize fundamental principles and important equations
- Cards should help students build deep understanding, not memorize trivia
- Example of BAD: "What does π represent in sin(2πx)?"
- Example of GOOD: "How does Fourier analysis decompose signals into frequency components?"

CONTEXT REQUIREMENTS:
- For equations: Explain what variables represent and their typical values/ranges
- For comparisons: State what is being compared to (e.g., "30 bins compared to typical 10-20 bins")
- For transformations: Describe the starting point and end result
- For examples: Provide the full setup, not just a fragment
- For technical terms: Include a brief definition if not commonly known

FORBIDDEN CONTENT - NEVER CREATE CARDS WITH:
- References to other papers: "According to Smith et al. [12]..." or "As shown in reference [7]..."
- ANY reference numbers: "ref. [6]", "[1]", "(Smith, 2023)", "the framework in [6]", "reference ^6", "^12", "^7"
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
❌ "What innovation did the framework described in reference ^6 bring?" (Remove reference number)
❌ "Describe how Lachapelle et al. approach causal inference" (Focus on the method, not the authors)
❌ "What does NAS stand for?" (Simple memorization - ask what NAS DOES instead)
❌ "The equation MathJax represents the maximum entropy solution" (No context about constraints)
❌ "A histogram with 30 bins shows higher entropy" (No comparison baseline)
❌ "How does the red curve help understanding?" (What red curve? No image reference allowed)

GOOD EXAMPLES WITH PROPER CONTEXT:
✓ "What transformation is applied in the causal inference framework that combines DAGs with deep learning?"
✓ "How does the multi-layer perceptron model handle missing data in the feature matrix?"
✓ "What is the advantage of combining causal inference with deep learning for dimensionality reduction?"
✓ "In maximum entropy estimation with moment constraints E[x]=μ and E[x²]=σ²+μ², what does the resulting distribution represent?"
✓ "When comparing probability distributions, why does a histogram spread over 30 bins (versus concentrated in 5-10 bins) indicate higher entropy?"
✓ "For the nonlinear transformation y₁ = tanh(x₁) and y₂ = x₂ + 0.1x₁², how does this affect the original Gaussian distribution?"

CLOZE DELETION CARD FORMAT (YOU MUST CREATE {num_cloze} OF THESE):
## [Self-contained statement with {{c1::hidden text}} that tests understanding]

- #tag1, #tag2

CRITICAL CLOZE FORMAT RULES:
1. ALL content including {{c1::...}} MUST be in the ## header line (the front)
2. NEVER put {{c1::...}} in the answer/back section
3. The back section should be EMPTY (it will only contain audio in post-processing)
4. Every cloze card MUST have tags on the "- #tag1, #tag2" line

IMPORTANT CLOZE RULES:
- CRITICAL: Cloze cards must be STATEMENTS, never questions (no "?" at the end)
  * ❌ WRONG: "How does X affect {{c1::Y}} in context Z?"
  * ✓ CORRECT: "X affects Y in context Z by {{c1::causing specific change}}"
- PRIORITIZE hiding definitions, technical terms, and difficult concepts
- Focus on terminology that students need to understand deeply
- Hide the MEANING or DEFINITION of complex terms, not just the term itself
- For equations: Hide what the equation REPRESENTS or key components
- CRITICAL: When mentioning an equation, the ENTIRE equation must be inside cloze markers
- Make cards educational - test understanding of concepts, not memorization
- Each card must stand alone without external context
- Focus on FUNDAMENTAL CONCEPTS from the document summary, not trivial details
- Avoid cards about minor notation or parameters that don't aid understanding

CLOZE CARD PRIORITIES (in order of importance):
1. Definitions of technical terms and jargon
2. What complex concepts mean or represent
3. Key properties or characteristics of methods/algorithms
4. Important relationships between concepts
5. Significance or purpose of equations/formulas
6. Critical distinctions between similar concepts

CRITICAL MATH CLOZE RULES:
- If you mention "the equation" followed by math, the ENTIRE equation goes inside {{c1::...}}
- NEVER write: "The equation {{c1::something}} \\(actual equation\\)"
- CORRECT: "The equation {{c1::\\(E[X_j | X_{pa(j)}] = g_j(f_j(X))\\)}} expresses..."
- For simple equations, you can hide parts: "The derivative \\(\\frac{d}{dx}(x^2) = {{c1::2x}}\\)"

Example GOOD cloze cards focusing on definitions and concepts:
## Regularization in machine learning refers to {{c1::techniques that add constraints or penalties to prevent overfitting by limiting model complexity}}.

- #machine-learning.regularization, #overfitting-prevention

## A Directed Acyclic Graph (DAG) is {{c1::a graph with directed edges and no cycles, meaning you cannot start at a node and follow edges to return to the same node}}.

- #graph-theory.dags, #data-structures

## The backpropagation algorithm works by {{c1::computing gradients of the loss function with respect to weights by applying the chain rule recursively from output to input layers}}.

- #neural-networks.training, #optimization.gradients

## In statistics, a p-value represents {{c1::the probability of obtaining test results at least as extreme as observed, assuming the null hypothesis is true}}.

- #statistics.hypothesis-testing, #p-values

## The vanishing gradient problem occurs when {{c1::gradients become exponentially small as they propagate backwards through many layers, preventing effective weight updates in deep networks}}.

- #deep-learning.challenges, #neural-networks.gradients

## Attention mechanisms in neural networks allow models to {{c1::dynamically focus on different parts of the input by computing weighted combinations based on learned relevance scores}}.

- #deep-learning.attention, #transformer-architecture

Example BAD cloze cards to AVOID:
- "How can the choice of axis impact {{c1::perception}} in public health contexts?" (Cloze card is a question!)
- "What does the term '30 excess deaths' mean based on {{c1::average risk comparisons}}?" (Questions are for Q&A cards, not cloze!)
- "According to [12], the algorithm is {{c1::efficient}}" (References external paper)
- "The original constraints are replaced by {{c1::continuous equality}}" (What original constraints?)
- "As shown in Figure 3, performance {{c1::improves}}" (No access to Figure 3)
- "The equation {{c1::describes relationships}} \\(E[X | Y] = f(Y)\\)" (Equation is outside cloze!)
- "Using equation {{c1::MathJax}} to express dependencies" (Meaningless placeholder)
- "The probability is \\[{{c1::p(x|\\mu,\\sigma^2) = \\frac{1}{\\sqrt{2\\pi\\sigma^2}}e^{-\\frac{(x-\\mu)^2}{2\\sigma^2}}}}\\]" (Display math inside cloze!)
- "The equation \\[p(t|x,w,\\sigma^2)={{c1::\\mathcal{N}(t|y(x,w),\\sigma^2)}}\\]" (Display math with cloze inside!)

CRITICAL FORMAT ERRORS TO AVOID:
❌ WRONG - Putting cloze in the back/answer:
## In visual data, what function transforms density modes?

{{c1::The sigmoid function}} transforms the modes.

- #visualization

❌ WRONG - Q&A format with cloze in answer:
## What is the probability of data in Bayesian inference?

The equation {{c1::\\(p(\\mathcal{D})=\\int p(\\mathcal{D} | \\mathbf{w}) p(\\mathbf{w}) \\, \\mathrm{d} \\mathbf{w}\\)}} represents the probability.

- #bayesian

✅ CORRECT - All content in the front with cloze:
## In visual data, {{c1::the sigmoid function}} transforms density modes as indicated by color curves.

- #visualization, #sigmoid

✅ CORRECT - Equation cloze all in front:
## In Bayesian inference, the probability of data is given by {{c1::\\(p(\\mathcal{D})=\\int p(\\mathcal{D} | \\mathbf{w}) p(\\mathbf{w}) \\, \\mathrm{d} \\mathbf{w}\\)}}.

- #bayesian-inference, #probability

GOOD alternatives for complex equations:
- "The Gaussian distribution has the form \\[p(x|\\mu,\\sigma^2) = \\frac{1}{\\sqrt{2\\pi\\sigma^2}}e^{-\\frac{(x-\\mu)^2}{2\\sigma^2}}\\] where the normalization factor is {{c1::1/\\sqrt{2\\pi\\sigma^2}}}"
- "In linear regression, we model \\(p(t|x,w,\\sigma^2) = \\mathcal{N}(t|y(x,w),\\sigma^2)\\), which means the target follows {{c1::a Gaussian distribution centered at the prediction y(x,w)}}"

REGULAR Q&A CARD FORMAT (YOU MUST CREATE {num_cards} OF THESE):
## [MUST BE A QUESTION - start with What/How/Why/When/Which/Calculate/Explain/Compare]

[Complete answer that doesn't reference external content]

- #tag1, #tag2

CRITICAL Q&A RULES:
- EVERY regular card MUST ask a question in the ## header
- NEVER use statements for regular cards (save statements for cloze cards only)
- Include all necessary context IN THE QUESTION
- Good question starters: "What is...", "How does...", "Why does...", "Calculate...", "Explain how...", "Compare..."
- BAD: "The significance of applying a change of variables to a Gaussian distribution"
- GOOD: "What is the significance of applying a change of variables to a Gaussian distribution?"

Example GOOD regular cards WITH CONTEXT:
## What is the time complexity of quicksort in the average case?

The average case time complexity of quicksort is O(n log n), where n is the number of elements to sort. This assumes random pivot selection and balanced partitions.

- #algorithms.sorting, #complexity-analysis

## How does gradient descent minimize a loss function?

Gradient descent iteratively updates parameters by moving in the direction opposite to the gradient. At each step, it computes the gradient of the loss function and updates parameters: θ = θ - α∇L(θ), where α is the learning rate.

- #optimization, #machine-learning.algorithms

## In polynomial regression with basis functions φⱼ(x) = xʲ for j=0 to M, how does the design matrix Φ relate inputs to the model?

The design matrix Φ has shape N×(M+1) where N is the number of data points. Each row i contains [1, xᵢ, xᵢ², ..., xᵢᴹ], transforming the input xᵢ into the polynomial basis. This allows linear regression in the transformed feature space.

- #regression.polynomial, #linear-algebra.matrices

## When using variational inference to approximate p(w|D) with q(w), what does the ELBO (evidence lower bound) represent?

The ELBO represents a lower bound on log p(D), the log marginal likelihood. It equals log p(D) - KL[q(w)||p(w|D)], so maximizing ELBO minimizes the KL divergence between the approximate and true posterior. It provides both a tractable optimization objective and a measure of approximation quality.

- #bayesian-inference.variational, #optimization.objectives

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
   IMPORTANT: Use hyphens (-) instead of underscores (_) in tags: #machine-learning NOT #machine_learning
6. Never start the question with the citation - it will be added automatically
7. EDUCATIONAL VALUE - PRIORITIZE creating cards about:
   - KEY CONCEPTS AND FUNDAMENTAL PRINCIPLES from the document
   - Mathematical equations that are IMPORTANT for understanding the subject
   - Core algorithms and their purpose (not minor implementation details)
   - Major theoretical results and their significance
   - Statistical methods and their applications
   - Avoid trivial notation questions (e.g., "what is π?") - focus on concepts
8. Use the document summary to identify WHAT'S IMPORTANT to teach
9. Use MathJax format: \\(...\\) for inline math, \\[...\\] for display math
10. NEVER use $ or $$ delimiters - Anki uses \\( \\) and \\[ \\]
11. NEVER use LaTeX tables (\\\\begin{{tabular}})
12. For cloze cards with math: If }} appears in your LaTeX, add a space before it
    Example: {{c1::The formula \\(\\frac{a}{\\frac{b}{c} }\\) shows...}} (note the space before })
13. For cloze cards with :: in content: Use HTML comment
    Example: {{c1::std:<!-- -->:variant is a C++ feature}}
14. For equation cloze cards: When referencing "the equation", include the ENTIRE equation in cloze
    Example: "The equation {{c1::\\(E = mc^2\\)}} demonstrates..." NOT "The equation {{c1::E=mc²}} \\(E = mc^2\\)..."
15. CRITICAL LaTeX/MathJax rules for cloze cards:
    - AVOID complex LaTeX inside cloze deletions - prefer simple expressions or conceptual answers
    - NEVER use display math \\[...\\] inside cloze - use inline \\(...\\) only
    - For complex equations, put the cloze around the CONCEPT, not the formula
    - Add parentheses around expressions: "1 - \\cos" → "(1 - \\cos)"
    - Fix summation indices: NOT "\\sum_{i=1}}^{m}}" but "\\sum_{i=1}^{m}"
    - Ensure balanced braces in LaTeX commands
    - Maximum 1 cloze deletion per card (use {{c1::}})
    - Keep entire mathematical expressions together in one cloze
    - NEVER split cloze deletions across multiple lines
16. Each card must teach a concept, not test memorization of references
17. IMPORTANT: Focus on mathematical notation that MATTERS for understanding key concepts
18. NEVER use generic tags like #equation, #formula, #definition, #concept, #method
    Use specific conceptual tags: #optimization.gradient-descent, #causal-inference.dag, #machine-learning.regularization
    TAG FORMAT RULES: Use hyphens (-) not underscores (_) or spaces. #deep-learning NOT #deep_learning or #deep learning
19. ALWAYS define mathematical symbols within the card: "where h is a smooth function" not just "h(W) = 0"
20. ALWAYS expand acronyms when first used: "NAS (Neural Architecture Search)" not just "NAS"
21. For EVERY mathematical symbol or function (h, F, g_j, etc.), ensure the card defines what it represents
22. Focus on WHAT methods do and HOW they work, not WHO proposed them
23. Transform author-centric questions into concept-centric ones:
    ❌ "What is Zheng et al.'s approach?" 
    ✓ "How does the nonparametric DAG learning method work?"

Start generating cards now. First generate all {num_cloze} cloze cards, then generate all {num_cards} regular cards.""",
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
{content}""",
                    },
                }
            },
        )

        cls._write_yaml(
            prompts_dir / "technical.yaml",
            {
                "prompts": {
                    "summary": {
                        "system": "You are an expert in technical and scientific literature.",
                        "document_summary": """Create a technical summary focusing on:
1. Mathematical formulations
2. Algorithm descriptions
3. Technical acronyms and notation
4. Implementation details
5. Experimental setup

{content}""",
                    }
                }
            },
        )

        # Models configs
        models_dir = config_dir / "models"
        models_dir.mkdir(exist_ok=True)

        cls._write_yaml(
            models_dir / "default.yaml",
            {
                "models": {
                    "llm": {
                        "provider": "openai",
                        "model": "gpt-5",
                        "temperature": 0.7,
                        "max_retries": 3,
                    },
                    "tts": {
                        "provider": "elevenlabs",
                        "voice_id": "21m00Tcm4TlvDq8ikWAM",  # Rachel
                        "model": "eleven_monolingual_v2",
                        "stability": 0.5,
                        "similarity_boost": 0.5,
                    },
                }
            },
        )

        cls._write_yaml(
            models_dir / "openai_tts.yaml",
            {
                "models": {
                    "tts": {
                        "provider": "openai",
                        "voice": "nova",
                        "model": "tts-1-hd",
                        "speed": 1.0,
                    }
                }
            },
        )

        # Audio configs
        audio_dir = config_dir / "audio"
        audio_dir.mkdir(exist_ok=True)

        cls._write_yaml(
            audio_dir / "default.yaml",
            {
                "audio": {
                    "generate_complementary": False,
                    "generate_summary": False,
                    "generate_reading": False,
                    "generate_lecture": False,
                    "complementary_speed": 1.6,
                    "summary_speed": 1.1,
                    "reading_speed": 1.2,
                    "lecture_speed": 1.1,
                    "format": "mp3",
                    "quality": "high",
                }
            },
        )

        # None - no audio generation (just for clarity)
        cls._write_yaml(
            audio_dir / "none.yaml",
            {
                "audio": {
                    "generate_complementary": False,
                    "generate_summary": False,
                    "generate_reading": False,
                    "generate_lecture": False,
                }
            },
        )

        # Essential - cards and summary only (most common use case)
        cls._write_yaml(
            audio_dir / "essential.yaml",
            {
                "audio": {
                    "generate_complementary": True,
                    "generate_summary": True,
                    "generate_reading": False,
                    "generate_lecture": False,
                    "complementary_speed": 1.6,
                    "summary_speed": 1.1,
                    "reading_speed": 1.2,
                    "lecture_speed": 1.1,
                    "format": "mp3",
                    "quality": "high",
                }
            },
        )

        # All but reading - complementary, summary, and lecture
        cls._write_yaml(
            audio_dir / "all_but_reading.yaml",
            {
                "audio": {
                    "generate_complementary": True,
                    "generate_summary": True,
                    "generate_reading": False,
                    "generate_lecture": True,
                    "complementary_speed": 1.6,
                    "summary_speed": 1.1,
                    "reading_speed": 1.2,
                    "lecture_speed": 1.1,
                    "format": "mp3",
                    "quality": "high",
                }
            },
        )

        # Full - all audio types
        cls._write_yaml(
            audio_dir / "full.yaml",
            {
                "audio": {
                    "generate_complementary": True,
                    "generate_summary": True,
                    "generate_reading": True,
                    "generate_lecture": True,
                    "complementary_speed": 1.6,
                    "summary_speed": 1.1,
                    "reading_speed": 1.2,
                    "lecture_speed": 1.1,
                    "format": "mp3",
                    "quality": "high",
                }
            },
        )

        # Output configs
        output_dir = config_dir / "output"
        output_dir.mkdir(exist_ok=True)

        cls._write_yaml(
            output_dir / "default.yaml",
            {
                "output": {
                    "base_dir": "swanki-out",
                    "formats": {
                        "cards_plain": "cards-plain.md",
                        "cards_audio": "cards-with-audio.md",
                        "cards_combined": "cards-combined.md",
                        "summary": "document-summary.md",
                    },
                    "organize_by_type": True,
                    "create_anki_deck": False,
                    "tag_format": "slugified",  # Options: "slugified", "spaces", "raw"
                }
            },
        )

        # Anki configs
        anki_dir = config_dir / "anki"
        anki_dir.mkdir(exist_ok=True)

        cls._write_yaml(
            anki_dir / "default.yaml",
            {
                "anki": {
                    "enabled": False,
                    "deck_name": "{deck_name}",  # Uses output_dir if specified, otherwise citation_key
                    "host": "127.0.0.1",
                    "port": 8765,
                    "auto_send": False,  # Whether to automatically send cards after generation
                    "update_existing": True,  # Whether to update existing cards
                    "media_upload": True,  # Whether to upload media files (images, audio)
                    "card_format": "with_audio",  # Options: "plain", "with_audio"
                }
            },
        )

        cls._write_yaml(
            anki_dir / "auto_send.yaml",
            {
                "anki": {
                    "enabled": True,
                    "auto_send": True,
                    "deck_name": "{deck_name}",  # Uses output_dir if specified, otherwise citation_key
                    "card_format": "with_audio",
                }
            },
        )

        cls._write_yaml(
            anki_dir / "custom_deck.yaml",
            {
                "anki": {
                    "enabled": True,
                    "deck_name": "Research::Papers::{deck_name}",  # Custom hierarchy with output_dir or citation_key
                    "auto_send": False,
                }
            },
        )

        # Refinement configs
        refinement_dir = config_dir / "refinement"
        refinement_dir.mkdir(exist_ok=True)

        cls._write_yaml(
            refinement_dir / "default.yaml",
            {
                "refinement": {
                    "enabled": True,  # Enabled by default for better card quality
                    "max_iterations": 3,
                    "early_exit_on_quality": 0.9,
                    # Content types to refine
                    "content_types": ["regular", "cloze", "image"],
                    # Whether to refine audio transcripts
                    "include_audio": False,
                    # Feedback prompts for different content types
                    "feedback_prompts": {
                        "regular_cards": """Check these regular cards for quality issues:
1. External references ([1], "According to X", "Figure 3")
2. Vague context ("this framework", "the model")
3. Generic tags (#equation vs #calculus.derivatives)
4. Author-centric questions ("What is Smith's method?")
5. Undefined mathematical symbols
6. Rote memorization questions
7. Educational relevance - does this help students learn KEY CONCEPTS?
   - BAD: "In the equation sin(2πx), what does π represent?"
   - GOOD: "How does the Fourier transform decompose signals into frequency components?"
8. Focus on fundamentals, not trivial notation details
9. Answer revealed in question

If ALL cards meet quality standards AND are educationally valuable, set done=True.
Otherwise list specific issues with card numbers.""",
                        "cloze_cards": """Check these cloze cards for issues:
1. CRITICAL: Cloze cards that ARE questions (end with "?")
   - BAD: "How does X affect {{c1::Y}} in context Z?"
   - BAD: "What is the impact of {{c1::30 excess deaths}}?"
   - GOOD: "X affects Y in context Z by {{c1::specific mechanism}}"
   - GOOD: "The term '30 excess deaths' means {{c1::30 more deaths than expected}}"
2. NOT focusing on definitions and difficult concepts
   - GOOD: Hiding what a term means or how a concept works
   - BAD: Hiding random facts or simple values
3. Educational relevance - does this help students learn KEY CONCEPTS?
   - Focus on fundamental principles, not trivial details
   - Test understanding of important concepts from the document
4. Cloze cards with additional questions after the cloze deletion
   - BAD: "The algorithm is {{c1::O(n log n)}}. Why is this important?"
   - GOOD: "The algorithm has time complexity {{c1::O(n log n)}}"
4. More than 1 cloze deletion per card (warning only)
5. Math equations split across cloze markers
6. Entire equations not inside cloze when referenced
7. Testing memorization instead of understanding
8. Missing or generic tags
9. Malformed LaTeX/MathJax within cloze deletions:
   - Missing parentheses around expressions (e.g., "1 - \\cos" should be "(1 - \\cos")
   - Extra closing braces in summations/fractions
   - Unbalanced braces or parentheses
   - Incorrect MathJax delimiters
10. CRITICAL: Display math \\[...\\] inside cloze deletions
    - BAD: "\\[{{c1::equation}}\\]" or "{{c1::\\[equation\\]}}"
    - GOOD: "{{c1::\\(equation\\)}}" for inline math
11. CRITICAL: Multiline cloze deletions (cloze split across lines)
    - Check if {{c1:: starts on one line but }} ends on another
12. Complex LaTeX inside cloze - prefer conceptual answers
    - BAD: {{c1::complex multi-line equation}}
    - GOOD: {{c1::a Gaussian distribution}} or {{c1::the normalization factor}}

Example of correct math cloze:
"The equation {{c1::\\(E = mc^2\\)}} shows..." (simple inline math)
"The Gaussian has normalization factor {{c1::1/\\sqrt{2\\pi\\sigma^2}}}" (simple part)
"This represents {{c1::a conditional probability distribution}}" (conceptual)

If ALL cards are correct AND educationally valuable, set done=True.""",
                        "image_cards": """Check these image-based cards:
1. Questions that just ask to describe the image
2. Image summaries that give away the answer
3. Image markdown included in text
4. Not testing understanding of concepts

Good questions test WHY/HOW, not just WHAT is shown.
If ALL cards meet standards, set done=True.""",
                        # Card audio transcripts - different for each card type
                        "regular_card_audio": """Check this REGULAR card audio transcript:
1. Math notation must be converted to natural language
2. Acronyms expanded on first use
3. Citation key pronounced clearly at start
4. Technical terms have pronunciation guides
5. Both front and back should be readable

If transcript is clear for audio, set done=True.""",
                        "cloze_card_audio": """Check this CLOZE card audio transcript:

FRONT audio must:
1. Replace ALL {{c1::text}} with "blank"
2. Citation key pronounced clearly at start
3. Math outside cloze converted to natural language

BACK audio must:
1. Read the COMPLETE text including cloze content
2. NO "blank" - reveal all hidden content
3. Math notation converted to natural language

If BOTH transcripts follow these rules, set done=True.""",
                        "image_card_audio": """Check this IMAGE card audio transcript:
1. Must include "Image description:" followed by full description
2. Image description must be detailed (what type, layout, components)
3. Math in image description converted to natural language
4. Question/answer audio includes the image context
5. Citation key pronounced clearly at start

If image is well-described for audio-only learning, set done=True.""",
                        # Document-level audio formats
                        "summary_audio": """Check this SUMMARY audio transcript:
1. Professional, informative tone
2. Citation key mentioned naturally early
3. All acronyms expanded
4. Math notation humanized
5. Focus on key contributions and findings

If summary is clear and professional, set done=True.""",
                        "reading_audio": """Check this READING audio transcript:
1. Full document narration
2. All math notation converted to words
3. Citation key mentioned at beginning
4. Figure/table descriptions included
5. Clear pronunciation of technical terms

If reading is complete and clear, set done=True.""",
                        "lecture_audio": """Check this LECTURE audio transcript:
1. Educational presentation style
2. Direct start without lengthy intro
3. Citation key mentioned naturally
4. Avoids theatrical language
5. Math and technical terms clearly explained

If lecture is educational and clear, set done=True.""",
                    },
                    # Refinement prompts for fixing issues
                    "refinement_prompts": {
                        "regular_cards": """Fix ALL the issues identified in the feedback.
Maintain the same number of cards.
Ensure every card is self-contained.
Use specific conceptual tags.""",
                        "cloze_cards": """Fix ALL cloze card issues:
- CRITICAL: Convert questions to statements:
  * If card ends with '?', rewrite as a statement
  * "How does X affect {{c1::Y}}?" → "X affects Y by {{c1::mechanism}}"
  * "What is the impact of {{c1::concept}}?" → "The impact of concept is {{c1::specific effect}}"
  * "Why does {{c1::phenomenon}} occur?" → "Phenomenon occurs because {{c1::reason}}"
- Reduce to max 1 cloze deletion (split cards if needed)
- Keep math equations together inside cloze markers
- Fix LaTeX/MathJax formatting:
  * Add missing parentheses: "1 - \\cos" → "(1 - \\cos)"
  * Fix double closing braces: "\\sum_{i=1}}^{m}}" → "\\sum_{i=1}^{m}"
  * Ensure balanced braces and parentheses
  * NEVER use display math \\[...\\] inside cloze - convert to inline \\(...)\\)
  * Join multiline cloze deletions into single lines
- For complex equations, prefer conceptual cloze:
  * BAD: {{c1::complex equation with many terms}}
  * GOOD: The equation [show equation] represents {{c1::a Gaussian distribution}}
- Avoid overly complex LaTeX in cloze - use simpler expressions or concepts
- Ensure understanding-based questions
- Add proper hierarchical tags""",
                        "image_cards": """Improve image cards to:
- Test conceptual understanding
- Avoid revealing answers in summaries
- Remove any image markdown
- Focus on WHY/HOW questions""",
                        # Card audio refinement prompts
                        "regular_card_audio": """Fix audio transcript for regular card:
- Convert ALL math notation to natural language
- Expand acronyms: "CNN" -> "Convolutional Neural Network (CNN)"
- Add pronunciation: "Dijkstra (DIKE-stra)"
- Ensure citation key is clear at start""",
                        "cloze_card_audio": """Fix CLOZE card audio transcripts:
FRONT: Replace ALL cloze content with "blank"
- {{c1::E = mc²}} -> "The equation blank shows..."
BACK: Read COMPLETE text with cloze content revealed
- "The equation E equals m c squared shows...\"""",
                        "image_card_audio": """Fix IMAGE card audio transcript:
- Add detailed image description at start
- "Image description: This figure shows a flowchart with..."
- Include all visual elements for audio-only learners
- Convert any math in descriptions to words""",
                        # Document audio refinement prompts
                        "summary_audio": """Refine summary audio:
- Professional tone throughout
- Natural citation key mention
- Expand all acronyms
- Focus on key findings""",
                        "reading_audio": """Refine reading audio:
- Complete document narration
- Describe all figures/tables
- Convert all math to speakable form
- Add section transitions""",
                        "lecture_audio": """Refine lecture audio:
- Educational, not theatrical
- Direct start, concise end
- Clear explanations
- Natural flow""",
                    },
                }
            },
        )

        cls._write_yaml(
            refinement_dir / "strict.yaml",
            {
                "refinement": {
                    "enabled": True,
                    "max_iterations": 5,
                    "early_exit_on_quality": 0.95,
                    "content_types": ["regular", "cloze", "image"],
                    "include_audio": True,
                }
            },
        )

        cls._write_yaml(
            refinement_dir / "minimal.yaml",
            {
                "refinement": {
                    "enabled": True,
                    "max_iterations": 1,
                    "early_exit_on_quality": 0.7,
                    "content_types": ["regular", "cloze"],
                    "include_audio": False,
                }
            },
        )

        cls._write_yaml(
            refinement_dir / "disabled.yaml", {"refinement": {"enabled": False}}
        )

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
        - Multiline strings use literal style (|) for readability
        """
        # Custom representer for multiline strings
        def str_representer(dumper, data):
            if '\n' in data:
                # Use literal style for multiline strings
                return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
            return dumper.represent_scalar('tag:yaml.org,2002:str', data)
        
        yaml.add_representer(str, str_representer)
        
        with open(path, "w") as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False, width=120)
