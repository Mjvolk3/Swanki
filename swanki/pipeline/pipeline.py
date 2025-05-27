from pathlib import Path
from typing import Dict, Any, List
from omegaconf import DictConfig
import instructor
from openai import OpenAI
import os
import random
import subprocess
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

from ..models import (
    DocumentSummary, CardGenerationResponse, 
    ImageSummary, ProcessingState, PlainCard
)

# Import new processing modules
from ..processing import (
    PDFProcessor,
    MarkdownConverter,
    MarkdownCleaner,
    ImageProcessor,
    AnkiProcessor
)

# Import audio utilities
from ..utils.audio import generate_card_audio, generate_summary_audio, generate_reading_audio

# Import content utilities
from ..utils.content import extract_images_from_markdown, detect_math_content, generate_image_card_prompts


class Pipeline:
    """Main processing pipeline with Hydra configuration"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.instructor = instructor.patch(OpenAI())
        self.state = None
        
        # Load environment variables
        load_dotenv()
        self.data_dir = Path(os.getenv('SWANKI_DATA', 'swanki-out'))
        
    def process_full(self, pdf_path: Path, citation_key: str) -> Dict[str, Path]:
        """Process PDF with configuration-driven pipeline"""
        
        # Initialize state
        self.state = ProcessingState(
            pdf_path=pdf_path,
            citation_key=citation_key,
            current_stage="initialization"
        )
        
        # Create output directory based on citation key with auto-increment if exists
        base_name = citation_key if citation_key else 'swanki-out'
        output_dir = self.data_dir / base_name
        
        # If directory exists, append a number
        if output_dir.exists():
            counter = 0
            while True:
                numbered_dir = self.data_dir / f"{base_name}_{counter}"
                if not numbered_dir.exists():
                    output_dir = numbered_dir
                    break
                counter += 1
        
        self.output_base = output_dir
        self.output_base.mkdir(parents=True, exist_ok=True)
        
        # 1. Split PDF based on config
        self.state.current_stage = "pdf_split"
        pages = self.split_pdf(pdf_path)
        
        # 2. Convert to markdown
        self.state.current_stage = "markdown_conversion"
        markdown_files = self.convert_to_markdown(pages)
        
        # Check if conversion was successful - fail fast if not
        if not markdown_files:
            raise RuntimeError("PDF to markdown conversion failed. Cannot proceed without markdown content.")
        
        # 3. Clean markdown
        self.state.current_stage = "markdown_cleaning"
        cleaned_files = self.clean_markdown(markdown_files)
        
        # 4. Process images
        self.state.current_stage = "image_processing"
        image_summaries = self.process_images(cleaned_files)
        
        # 5. Generate document summary (EARLY!)
        self.state.current_stage = "summary_generation"
        doc_summary = self.generate_document_summary(
            cleaned_files,
            image_summaries
        )
        self.state.document_summary = doc_summary
        
        # 6. Generate cards with sliding window
        self.state.current_stage = "card_generation"
        pipeline_config = self.config.get('pipeline', {})
        processing_config = pipeline_config.get('processing', {})
        all_cards = self.generate_cards_with_window(
            cleaned_files,
            doc_summary,
            window_size=processing_config.get('window_size', 2),
            skip=processing_config.get('skip', 1),
            num_cards=processing_config.get('num_cards_per_page', 3)
        )
        
        # 6.5. Generate image cards if enabled
        image_config = processing_config.get('image_cards', {})
        if image_config.get('enabled', True):
            self.state.current_stage = "image_card_generation"
            image_cards = self.generate_image_cards(
                cleaned_files,
                doc_summary,
                cards_per_image=image_config.get('cards_per_image', 3),
                image_on_front=image_config.get('image_on_front', True),
                image_on_back=image_config.get('image_on_back', True),
                require_math=image_config.get('require_math_content', False),
                placement_strategy=image_config.get('placement_strategy', 'smart'),
                front_back_ratio=image_config.get('front_back_ratio', 0.5)
            )
            all_cards.extend(image_cards)
        
        # 7. Store citation key for later use
        self.citation_key = citation_key
        
        self.state.cards_generated = len(all_cards)
        
        # 8. Generate outputs based on config
        self.state.current_stage = "output_generation"
        outputs = self.generate_outputs(all_cards, doc_summary, self.output_base)
        
        # 9. Generate audio if configured
        audio_config = self.config.get('audio', {}).get('audio', {})
        if any([
            audio_config.get('generate_complementary', False),
            audio_config.get('generate_summary', False),
            audio_config.get('generate_reading', False)
        ]):
            self.state.current_stage = "audio_generation"
            self.generate_audio(all_cards, doc_summary, outputs, cleaned_files)
        
        # 10. Send to Anki if configured
        anki_config = self.config.get('anki', {}).get('anki', {})
        if anki_config.get('enabled', False) and anki_config.get('auto_send', False):
            self.state.current_stage = "anki_sending"
            self.send_to_anki(all_cards, outputs, anki_config)
        
        self.state.outputs = outputs
        return outputs
    
    def split_pdf(self, pdf_path: Path) -> List[Path]:
        """Split PDF into individual pages using PDFProcessor"""
        pdf_processor = PDFProcessor(self.output_base)
        pdf_files = pdf_processor.split_pdf(pdf_path)
        return pdf_files
    
    def convert_to_markdown(self, pages: List[Path]) -> List[Path]:
        """Convert individual PDF pages to markdown using MarkdownConverter"""
        
        # Create output directory
        md_singles_dir = self.output_base / "md-singles"
        md_singles_dir.mkdir(parents=True, exist_ok=True)
        
        markdown_files = []
        
        logger.info(f"Converting {len(pages)} PDF pages to markdown")
        
        # Convert each page individually (like the legacy approach)
        for page_pdf in pages:
            # Create corresponding markdown filename
            md_filename = page_pdf.stem + ".md"  # page-1.pdf -> page-1.md
            md_path = md_singles_dir / md_filename
            
            # Use os.system approach which handles clearLine errors better
            cmd = f"mpx convert '{page_pdf}' '{md_path}'"
            
            logger.debug(f"Converting {page_pdf.name} to {md_path.name}")
            
            try:
                # Use os.system - it handles TTY issues better than subprocess
                exit_code = os.system(cmd)
                
                if exit_code == 0 and md_path.exists() and md_path.stat().st_size > 0:
                    logger.debug(f"Successfully converted {page_pdf.name}")
                    markdown_files.append(md_path)
                else:
                    logger.warning(f"Failed to convert {page_pdf.name} - exit code: {exit_code}")
                    
            except Exception as e:
                logger.error(f"Error converting {page_pdf.name}: {e}")
        
        if not markdown_files:
            raise RuntimeError("Failed to convert any PDF pages to markdown.")
        
        logger.info(f"Successfully converted {len(markdown_files)} pages to markdown")
        return sorted(markdown_files)
    
    def clean_markdown(self, markdown_files: List[Path]) -> List[Path]:
        """Clean markdown files using MarkdownCleaner"""
        cleaner = MarkdownCleaner(self.output_base)
        cleaned_files = cleaner.clean_all_markdown_files()
        return cleaned_files
    
    def process_images(self, markdown_files: List[Path]) -> List[ImageSummary]:
        """Process images and generate summaries using ImageProcessor"""
        # Initialize processor with OpenAI client if available
        processor = ImageProcessor(self.output_base, self.instructor)
        
        # Process all images
        image_infos = processor.process_all_images()
        
        # Convert to ImageSummary objects
        image_summaries = []
        for idx, info in enumerate(image_infos):
            if 'summary' in info:
                image_summary = ImageSummary(
                    image_url=info['url'],
                    summary=info['summary'],
                    alt_text=info.get('alt_text', ''),
                    page_idx=idx,
                    context=info.get('context', '')
                )
                image_summaries.append(image_summary)
        
        return image_summaries
    
    def generate_document_summary(
        self, 
        markdown_files: List[Path],
        image_summaries: List[ImageSummary]
    ) -> DocumentSummary:
        """Generate comprehensive document summary"""
        # Combine all markdown content
        combined_content = "\\n\\n".join([
            f.read_text() for f in markdown_files
        ])
        
        # Format image summaries
        image_summary_text = "\\n".join([
            f"Image {img.page_idx}: {img.summary}" 
            for img in image_summaries
        ])
        
        # Get prompts from config (note the nested structure)
        prompts_config = self.config.get('prompts', {}).get('prompts', {})
        summary_prompts = prompts_config.get('summary', {})
        system_prompt = summary_prompts.get('system', "You are an expert at creating concise, informative summaries of academic documents.")
        user_prompt = summary_prompts.get('document_summary', """Create a comprehensive summary of this document.
Focus on:
1. Main thesis and key contributions
2. All acronyms and their full forms
3. Technical terms that need clear definitions
4. Methodology and approach
5. Key findings

Document content:
{content}

Image summaries:
{image_summaries}""")
        
        # Generate summary using instructor
        models_config = self.config.get('models', {}).get('models', {})
        llm_config = models_config.get('llm', {})
        response = self.instructor.chat.completions.create(
            model=llm_config.get('model', 'gpt-4'),
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": user_prompt.format(
                        content=combined_content,
                        image_summaries=image_summary_text
                    )
                }
            ],
            response_model=DocumentSummary,
            max_retries=llm_config.get('max_retries', 3)
        )
        
        return response
    
    def generate_cards_with_window(
        self, 
        markdown_files: List[Path],
        doc_summary: DocumentSummary,
        window_size: int,
        skip: int,
        num_cards: int
    ) -> List[PlainCard]:
        """Generate cards using sliding window approach"""
        all_cards = []
        
        for i in range(0, len(markdown_files) - window_size + 1, skip):
            window_files = markdown_files[i:i + window_size]
            
            # Combine content from window
            combined_content = "\\n\\n".join([
                f.read_text() for f in window_files
            ])
            
            # Get config values
            prompts_config = self.config.get('prompts', {}).get('prompts', {})
            cards_prompts = prompts_config.get('cards', {})
            models_config = self.config.get('models', {}).get('models', {})
            llm_config = models_config.get('llm', {})
            processing_config = self.config.get('processing', {}).get('processing', {})
            
            # Generate cards for this window
            response = self.instructor.chat.completions.create(
                model=llm_config.get('model', 'gpt-4'),
                messages=[
                    {
                        "role": "system", 
                        "content": cards_prompts.get('system', "You are an expert at creating educational flashcards that test understanding.")
                    },
                    {
                        "role": "user",
                        "content": cards_prompts.get('generate_cards', 'Create {num_cards} flashcards from this content.').format(
                            num_cards=num_cards * len(window_files),
                            num_cloze=processing_config.get('cloze_cards_per_page', 2) * len(window_files),
                            title=doc_summary.title,
                            acronyms=doc_summary.acronyms,
                            technical_terms=doc_summary.technical_terms,
                            content=combined_content
                        )
                    }
                ],
                response_model=CardGenerationResponse,
                max_retries=llm_config.get('max_retries', 3)
            )
            
            all_cards.extend(response.cards)
        
        return all_cards
    
    def generate_image_cards(
        self,
        markdown_files: List[Path],
        doc_summary: DocumentSummary,
        cards_per_image: int = 3,
        image_on_front: bool = True,
        image_on_back: bool = True,
        require_math: bool = False,
        placement_strategy: str = "smart",
        front_back_ratio: float = 0.5
    ) -> List[PlainCard]:
        """Generate cards specifically for images found in the markdown files"""
        image_cards = []
        
        for file_path in markdown_files:
            content = file_path.read_text()
            
            # Extract images from this file
            images = extract_images_from_markdown(content, file_path.parent)
            
            for image_info in images:
                # Check if math content is required and present
                if require_math and not detect_math_content(image_info['context']):
                    continue
                
                print(f"Generating {cards_per_image} cards for image: {image_info['path']}")
                
                # Get surrounding content (more context around the image)
                file_content = content
                
                # Generate prompts for image cards
                prompts_config = self.config.get('prompts', {}).get('prompts', {})
                cards_prompts = prompts_config.get('cards', {})
                models_config = self.config.get('models', {}).get('models', {})
                llm_config = models_config.get('llm', {})
                
                # Create a specialized prompt for image cards
                image_prompt = f"""Create {cards_per_image} educational flashcards based on this image and its context.

Image Information:
- Path: {image_info['path']}
- Alt text: {image_info['alt']}
- Context: {image_info['context']}

Document Summary Context:
- Title: {doc_summary.title}
- Acronyms: {doc_summary.acronyms}
- Technical terms: {doc_summary.technical_terms}

Full content from this page:
{file_content}

Requirements:
- Each card should test understanding of the image content
- Cards can reference specific parts of the image (e.g., "What does the graph in the upper left show?")
- Include mathematical notation if present in the image
- Make questions specific to visual elements
- {'Image can appear on front or back of card as appropriate' if image_on_front and image_on_back else 'Image should appear on front of card' if image_on_front else 'Image should appear on back of card' if image_on_back else 'No image placement preference'}

FORMAT RULES:
1. Use ## for the question (front of card)
2. Answer goes on the next line (back of card)
3. Tags go as a single bullet: - #tag1, #tag2, #tag3
4. Use period-delimited tags from broad to narrow (e.g., #biology.cell-biology, #figures.graphs)
5. Include visual/image-related tags like #figures, #diagrams, #graphs, #charts as appropriate

Example card for an image:
## What does Figure 1 show about the relationship between X and Y?

Figure 1 demonstrates a positive correlation between X and Y, with the data points following a clear linear trend. The graph shows that as X increases from 0 to 10, Y increases proportionally from 2 to 20.

- #figures.graphs, #data-analysis.correlation, #statistics.linear-relationships"""

                # Generate cards using instructor
                try:
                    response = self.instructor.chat.completions.create(
                        model=llm_config.get('model', 'gpt-4'),
                        messages=[
                            {
                                "role": "system", 
                                "content": cards_prompts.get('system', "You are an expert at creating educational flashcards that test understanding of visual content.")
                            },
                            {
                                "role": "user",
                                "content": image_prompt
                            }
                        ],
                        response_model=CardGenerationResponse,
                        max_retries=llm_config.get('max_retries', 3)
                    )
                    
                    # Add image paths to the generated cards
                    for idx, card in enumerate(response.cards):
                        # Decide where to place the image based on config
                        if image_on_front and not image_on_back:
                            card.front.image_path = image_info['original_path']
                        elif image_on_back and not image_on_front:
                            card.back.image_path = image_info['original_path']
                        elif image_on_front and image_on_back:
                            # Both allowed, but NEVER put the same image on both sides
                            place_on_front = False
                            
                            if placement_strategy == "smart":
                                # Place on front if question references the image
                                place_on_front = any(word in card.front.text.lower() 
                                                   for word in ['figure', 'image', 'graph', 
                                                              'chart', 'diagram', 'show', 
                                                              'illustrate', 'depict', 'visual'])
                            elif placement_strategy == "alternate":
                                # Alternate between front and back
                                place_on_front = (idx % 2 == 0)
                            elif placement_strategy == "random":
                                # Random with specified ratio
                                place_on_front = random.random() < front_back_ratio
                            elif placement_strategy == "prefer_front":
                                place_on_front = True
                            elif placement_strategy == "prefer_back":
                                place_on_front = False
                            
                            # Place image on ONLY ONE side
                            if place_on_front:
                                card.front.image_path = image_info['original_path']
                                # Explicitly ensure it's not on the back
                                card.back.image_path = None
                            else:
                                card.back.image_path = image_info['original_path']
                                # Explicitly ensure it's not on the front
                                card.front.image_path = None
                    
                    image_cards.extend(response.cards)
                    
                    # Debug output for image placement
                    front_count = sum(1 for card in response.cards if card.front.image_path)
                    back_count = sum(1 for card in response.cards if card.back.image_path)
                    print(f"Generated {len(response.cards)} cards for image {image_info['path']}")
                    print(f"  Image placement - Front: {front_count}, Back: {back_count} (strategy: {placement_strategy})")
                    
                except Exception as e:
                    print(f"Error generating cards for image {image_info['path']}: {e}")
                    continue
        
        return image_cards
    
    def generate_outputs(
        self, 
        cards: List[PlainCard], 
        summary: DocumentSummary,
        output_dir: Path
    ) -> Dict[str, Path]:
        """Generate multiple output files based on config"""
        outputs = {}
        
        # Get output config
        output_config = self.config.get('output', {}).get('output', {})
        formats = output_config.get('formats', {})
        tag_format = output_config.get('tag_format', 'slugified')
        
        # Plain cards (no audio)
        plain_path = output_dir / formats.get('cards_plain', 'cards-plain.md')
        with open(plain_path, 'w') as f:
            for card in cards:
                f.write(card.to_md(
                    include_audio=False, 
                    citation_key=self.citation_key,
                    tag_format=tag_format
                ))
        outputs['cards_plain'] = plain_path
        
        # Only create cards with audio if complementary audio is enabled
        audio_config = self.config.get('audio', {}).get('audio', {})
        if audio_config.get('generate_complementary', False):
            # Cards with audio placeholders
            audio_path = output_dir / formats.get('cards_audio', 'cards-with-audio.md')
            with open(audio_path, 'w') as f:
                for i, card in enumerate(cards):
                    # Audio files will be generated with card index starting from 1
                    # Include citation key in filename to avoid conflicts
                    audio_front_uri = f"{self.citation_key}/gen-md-complementary-audio/{self.citation_key}_page-{i+1}_{i+1}_front.mp3"
                    audio_back_uri = f"{self.citation_key}/gen-md-complementary-audio/{self.citation_key}_page-{i+1}_{i+1}_back.mp3"
                    f.write(card.to_md(
                        include_audio=True, 
                        audio_front_uri=audio_front_uri,
                        audio_back_uri=audio_back_uri,
                        citation_key=self.citation_key,
                        tag_format=tag_format
                    ))
            outputs['cards_audio'] = audio_path
        
        # Document summary
        summary_path = output_dir / formats.get('summary', 'document-summary.md')
        with open(summary_path, 'w') as f:
            f.write(f"# {summary.title}\\n\\n")
            f.write(f"**Authors:** {', '.join(summary.authors)}\\n\\n")
            f.write(f"## Summary\\n\\n{summary.summary}\\n\\n")
            f.write(f"## Key Contributions\\n\\n")
            for contrib in summary.key_contributions:
                f.write(f"- {contrib}\\n")
            f.write(f"\\n## Acronyms\\n\\n")
            for acronym, definition in summary.acronyms.items():
                f.write(f"- **{acronym}**: {definition}\\n")
        outputs['summary'] = summary_path
        
        return outputs
    
    def generate_audio(
        self, 
        cards: List[PlainCard], 
        summary: DocumentSummary,
        outputs: Dict[str, Path],
        cleaned_files: List[Path]
    ):
        """Generate audio files based on configuration"""
        audio_config = self.config.get('audio', {}).get('audio', {})
        
        # Get API keys
        elevenlabs_api_key = os.getenv("ELEVEN_LABS_API_KEY")
        if not elevenlabs_api_key:
            raise RuntimeError("ELEVEN_LABS_API_KEY not set in environment.")
        
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise RuntimeError("OPENAI_API_KEY not set in environment.")
        openai_client = OpenAI(api_key=openai_api_key)
        
        # Get model config
        models_config = self.config.get('models', {}).get('models', {})
        llm_config = models_config.get('llm', {})
        model = llm_config.get('model', 'gpt-4o')
        voice_id = audio_config.get('voice_id')
        
        # Generate complementary audio (card audio)
        if audio_config.get('generate_complementary', False):
            print("Generating complementary audio...")
            audio_dir = self.output_base / "gen-md-complementary-audio"
            audio_dir.mkdir(exist_ok=True)
            
            for i, card in enumerate(cards):
                page_base = f"page-{i+1}"
                
                front_filename, back_filename = generate_card_audio(
                    card=card,
                    card_index=i+1,
                    page_base=page_base,
                    audio_dir=audio_dir,
                    openai_client=openai_client,
                    elevenlabs_api_key=elevenlabs_api_key,
                    voice_id=voice_id,
                    model=model,
                    citation_key=self.citation_key,
                )
                
                if back_filename:
                    print(f"Generated audio for card {i+1}: {front_filename}, {back_filename}")
                else:
                    print(f"Generated audio for cloze card {i+1}: {front_filename} (no back audio)")
        
        # Generate summary audio
        if audio_config.get('generate_summary', False):
            print("Generating summary audio...")
            summary_text = f"{summary.summary}\n\nKey Contributions:\n" + "\n".join([f"- {contrib}" for contrib in summary.key_contributions])
            summary_audio_path = self.output_base / "document-summary-audio.mp3"
            
            generate_summary_audio(
                summary_text=summary_text,
                output_path=summary_audio_path,
                openai_client=openai_client,
                elevenlabs_api_key=elevenlabs_api_key,
                voice_id=voice_id,
                model=model,
                citation_key=self.citation_key,
            )
            print(f"Generated summary audio: {summary_audio_path.name}")
        
        # Generate reading audio (full document)
        if audio_config.get('generate_reading', False):
            print("Generating reading audio...")
            # Combine all cleaned markdown content
            full_content = "\n\n".join([f.read_text() for f in cleaned_files])
            reading_audio_path = self.output_base / "document-reading-audio.mp3"
            
            generate_reading_audio(
                full_content=full_content,
                output_path=reading_audio_path,
                openai_client=openai_client,
                elevenlabs_api_key=elevenlabs_api_key,
                voice_id=voice_id,
                model=model,
                citation_key=self.citation_key,
            )
            print(f"Generated reading audio: {reading_audio_path.name}")
    
    def format_deck_name(self, template: str, citation_key: str) -> str:
        """Format deck name template with variables."""
        # Support template variables like {citation_key}
        variables = {
            'citation_key': citation_key or 'default'
        }
        
        # Replace template variables
        formatted = template
        for var, value in variables.items():
            formatted = formatted.replace(f"{{{var}}}", value)
        
        return formatted
    
    def prepare_anki_file(self, cards: List[PlainCard], deck_name: str, output_path: Path, include_audio: bool = True) -> Path:
        """Prepare markdown file for Anki with proper deck header."""
        anki_file = output_path.parent / f"anki-{output_path.name}"
        
        # First, read the existing output file to use its exact format
        # This ensures we preserve the exact card format that was generated
        with open(output_path, 'r') as f:
            content = f.read()
        
        with open(anki_file, 'w') as f:
            # Write deck name header (required by md_to_anki.py)
            f.write(f"# {deck_name}\n\n")
            
            # Write the rest of the content as-is
            # This preserves the exact tag format from the original file
            f.write(content)
        
        return anki_file
    
    def send_to_anki(self, cards: List[PlainCard], outputs: Dict[str, Path], anki_config: Dict[str, Any]):
        """Send cards to Anki using the modern AnkiProcessor."""
        try:
            # Format deck name with template variables
            deck_template = anki_config.get('deck_name', '{citation_key}')
            deck_name = self.format_deck_name(deck_template, self.citation_key)
            
            logger.info(f"Sending cards to Anki deck: {deck_name}")
            
            # Choose which output file to use as base
            # Important: Only use audio cards if they actually exist
            card_format = anki_config.get('card_format', 'with_audio')
            if card_format == 'with_audio' and 'cards_audio' in outputs:
                base_file = outputs['cards_audio']
            else:
                # Fall back to plain cards if audio cards don't exist or not requested
                base_file = outputs['cards_plain']
            
            # Prepare Anki file with proper deck header
            # Only include audio if it was actually generated
            use_audio = (card_format == 'with_audio' and 'cards_audio' in outputs)
            anki_file = self.prepare_anki_file(cards, deck_name, base_file, include_audio=use_audio)
            
            # Initialize AnkiProcessor
            host = anki_config.get('host', '127.0.0.1')
            port = anki_config.get('port', 8765)
            anki_processor = AnkiProcessor(host, port)
            
            # Send cards to Anki
            cards_added, cards_updated = anki_processor.send_cards_from_file(
                file_path=anki_file,
                deck_name=deck_name,
                update_existing=anki_config.get('update_existing', True),
                upload_media=anki_config.get('media_upload', True),
                sync_after=anki_config.get('sync_after', False)
            )
            
            logger.info(f"Successfully sent to Anki deck '{deck_name}': {cards_added} added, {cards_updated} updated")
            
        except Exception as e:
            logger.error(f"Failed to send cards to Anki: {e}")
            raise