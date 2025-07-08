"""Image processing module for handling images in markdown files.

This module processes images found in markdown files, generates summaries
for them using AI, and manages image-related operations in the pipeline.
Supports extracting images from markdown, generating AI summaries, and
downloading remote images.

Classes
-------
ImageProcessor
    Handles image extraction, summarization, and processing

Examples
--------
>>> from swanki.processing import ImageProcessor
>>> from pathlib import Path
>>> from openai import OpenAI
>>> 
>>> processor = ImageProcessor(
...     output_base=Path("output"),
...     openai_client=OpenAI()
... )
>>> images = processor.process_all_images()
>>> print(f"Processed {len(images)} images")
Processed 15 images
"""
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import re
import logging
from urllib.parse import unquote
import shutil
from openai import OpenAI
import os
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


class ImageProcessor:
    """Handles image extraction, summarization, and processing.
    
    Processes images found in markdown files by extracting them,
    generating AI-powered summaries using GPT-4 Vision, and managing
    image files. Supports both local and remote images.
    
    Parameters
    ----------
    output_base : Path
        Base directory for all output files
    openai_client : OpenAI, optional
        OpenAI client for image summarization. If not provided,
        will attempt to create one from environment variables.
    
    Attributes
    ----------
    output_base : Path
        Base output directory
    clean_md_singles_dir : Path
        Directory containing cleaned markdown files
    image_summaries_dir : Path
        Directory for image summaries
    images_dir : Path
        Directory for downloaded images
    openai_client : OpenAI or None
        Client for AI summarization
    
    Methods
    -------
    process_all_images()
        Process all images in cleaned markdown files
    process_images_in_file(md_path)
        Process images in a single markdown file
    download_remote_images(images)
        Download remote images to local storage
    
    Examples
    --------
    >>> processor = ImageProcessor(Path("output"))
    >>> 
    >>> # Process all images
    >>> all_images = processor.process_all_images()
    >>> 
    >>> # Process single file
    >>> images = processor.process_images_in_file(Path("page-1.md"))
    >>> 
    >>> # Download remote images
    >>> processor.download_remote_images(images)
    """
    
    def __init__(self, output_base: Path, openai_client: Optional[OpenAI] = None):
        """Initialize image processor.
        
        Parameters
        ----------
        output_base : Path
            Base directory for all output files. Will create subdirectories
            for image summaries and downloaded images.
        openai_client : OpenAI, optional
            OpenAI client for image summarization. If None, will attempt
            to create from OPENAI_API_KEY environment variable.
        
        Notes
        -----
        If no OpenAI client is provided and no API key is found,
        image summarization will be skipped but other processing
        will continue.
        """
        self.output_base = output_base
        self.clean_md_singles_dir = output_base / "clean-md-singles"
        self.image_summaries_dir = output_base / "image-summaries"
        self.images_dir = output_base / "images"
        
        # Initialize OpenAI client if not provided
        if openai_client is None:
            load_dotenv()
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                self.openai_client = OpenAI(api_key=api_key)
            else:
                self.openai_client = None
                logger.warning("OpenAI API key not found. Image summarization will be skipped.")
        else:
            self.openai_client = openai_client
    
    def process_all_images(self) -> List[Dict[str, any]]:
        """Process all images found in cleaned markdown files.
        
        Processes all markdown files in the clean-md-singles directory,
        extracting images and generating summaries for each.
        
        Returns
        -------
        List[Dict[str, any]]
            List of image information dictionaries containing:
            - url: Image URL or path
            - alt_text: Alternative text
            - context: Surrounding text context
            - summary: Generated AI summary (if available)
            - source_file: Source markdown filename
        
        Examples
        --------
        >>> processor = ImageProcessor(Path("output"))
        >>> images = processor.process_all_images()
        >>> for img in images:
        ...     print(f"{img['source_file']}: {img['alt_text']}")
        page-1.md: Figure 1
        page-2.md: Graph showing results
        """
        # Create output directories
        self.image_summaries_dir.mkdir(parents=True, exist_ok=True)
        # Only create images_dir if we actually need to download images
        # self.images_dir.mkdir(parents=True, exist_ok=True)  # Removed to prevent empty directory
        
        # Get all markdown files
        md_files = sorted(self.clean_md_singles_dir.glob("*.md"))
        
        all_images = []
        for md_file in md_files:
            images = self.process_images_in_file(md_file)
            all_images.extend(images)
        
        logger.info(f"Processed {len(all_images)} images total")
        return all_images
    
    def process_images_in_file(self, md_path: Path) -> List[Dict[str, any]]:
        """Process all images in a single markdown file.
        
        Extracts images from the markdown file, generates AI summaries,
        and optionally inserts summaries back into the content.
        
        Parameters
        ----------
        md_path : Path
            Path to the markdown file to process
        
        Returns
        -------
        List[Dict[str, any]]
            List of processed image information dictionaries
        
        Notes
        -----
        If summaries are generated, creates a new file with
        '_with_summaries' suffix containing the updated content.
        """
        if not md_path.exists():
            logger.error(f"Markdown file not found: {md_path}")
            return []
        
        content = md_path.read_text(encoding='utf-8')
        
        # Extract all images from the markdown
        images = self._extract_images_from_markdown(content, md_path)
        
        # Process each image
        processed_images = []
        for idx, image_info in enumerate(images):
            # Generate summary if OpenAI client is available
            # Process both remote (http) and local images
            if self.openai_client:
                try:
                    summary = self._generate_image_summary(image_info)
                    if summary:
                        image_info['summary'] = summary
                        
                        # Save summary to file
                        summary_filename = f"{md_path.stem}_{idx+1}.md"
                        summary_path = self.image_summaries_dir / summary_filename
                        summary_path.write_text(summary, encoding='utf-8')
                        image_info['summary_path'] = summary_path
                    else:
                        error_msg = f"No summary generated for image: {image_info['url']}"
                        logger.error(error_msg)
                        raise RuntimeError(error_msg)
                except Exception as e:
                    error_msg = f"Failed to generate summary for image {image_info['url']}: {e}"
                    logger.error(error_msg)
                    raise RuntimeError(error_msg)
            
            # Update content with summary if available
            if 'summary' in image_info:
                content = self._insert_image_summary(content, image_info)
            
            processed_images.append(image_info)
        
        # Save updated content if summaries were added
        if any('summary' in img for img in processed_images):
            updated_path = self.image_summaries_dir / f"{md_path.stem}_with_summaries.md"
            updated_path.write_text(content, encoding='utf-8')
        
        return processed_images
    
    def _extract_images_from_markdown(self, content: str, source_path: Path) -> List[Dict[str, any]]:
        """Extract all images from markdown content.
        
        Parameters
        ----------
        content : str
            Markdown content to parse
        source_path : Path
            Path to the source markdown file
        
        Returns
        -------
        List[Dict[str, any]]
            List of image information dictionaries with metadata
        
        Notes
        -----
        Extracts images in markdown format: ![alt](url)
        Captures 200 characters of context before and after each image.
        """
        images = []
        
        # Pattern for markdown images: ![alt](url)
        image_pattern = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')
        
        for match in image_pattern.finditer(content):
            alt_text = match.group(1)
            url = match.group(2)
            
            # Clean the URL
            cleaned_url = self._clean_image_url(url)
            
            # Get context around the image
            start = max(0, match.start() - 200)
            end = min(len(content), match.end() + 200)
            context = content[start:end].strip()
            
            image_info = {
                'alt_text': alt_text,
                'url': cleaned_url,
                'original_url': url,
                'context': context,
                'source_file': source_path.name,
                'position': match.start(),
                'match_text': match.group(0)
            }
            
            images.append(image_info)
        
        logger.debug(f"Found {len(images)} images in {source_path.name}")
        return images
    
    def _clean_image_url(self, url: str) -> str:
        """Clean and normalize image URLs.
        
        Args:
            url: Original URL string
            
        Returns:
            Cleaned URL
        """
        # Remove backslashes and decode URL encoding
        cleaned = unquote(url.replace("\\", "").replace("\n", "").strip())
        return cleaned
    
    def _generate_image_summary(self, image_info: Dict[str, any]) -> Optional[str]:
        """Generate a summary for an image using GPT-4 Vision.
        
        Uses AI to analyze the image and generate a descriptive summary
        based on the visual content and surrounding context.
        
        Parameters
        ----------
        image_info : Dict[str, any]
            Dictionary containing image URL and context
        
        Returns
        -------
        str or None
            Generated summary text (2-4 sentences), or None if failed
        
        Notes
        -----
        Requires OpenAI client with GPT-4 Vision access.
        Uses low temperature (0.3) for consistent summaries.
        """
        if not self.openai_client:
            return None
        
        try:
            # Build the prompt
            prompt = f"""Please analyze this image and provide a comprehensive summary.

Context around the image: {image_info['context']}

Describe:
1. What the image shows (diagrams, graphs, equations, etc.)
2. Key information or data presented
3. How it relates to the surrounding text
4. Any important details that would help understand the content

Keep the summary concise but informative (2-4 sentences)."""

            # For local images, we need to read the file and encode it
            image_url = image_info['url']
            
            # Check if it's a local image
            if not image_url.startswith('http'):
                # Try to find the image file
                # First, check if it's a relative path from the markdown file location
                source_dir = self.clean_md_singles_dir
                possible_paths = [
                    source_dir / image_url,  # Direct path
                    source_dir.parent / image_url,  # Parent directory
                    self.output_base / image_url,  # From output base
                    Path(image_url)  # Absolute path
                ]
                
                image_path = None
                for path in possible_paths:
                    if path.exists() and path.is_file():
                        image_path = path
                        break
                
                if not image_path:
                    logger.error(f"Local image not found: {image_url}")
                    return None
                
                # Read and encode the image
                import base64
                with open(image_path, 'rb') as img_file:
                    image_data = base64.b64encode(img_file.read()).decode('utf-8')
                
                # Use data URL for local images
                mime_type = "image/png" if image_path.suffix.lower() == '.png' else "image/jpeg"
                image_url = f"data:{mime_type};base64,{image_data}"

            # Add retry logic for image summary generation
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    response = self.openai_client.chat.completions.create(
                        model="gpt-4o",  # or "gpt-4-vision-preview" if using older API
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": prompt},
                                    {"type": "image_url", "image_url": {"url": image_url}}
                                ]
                            }
                        ],
                        max_tokens=300,
                        temperature=0.3
                    )
                    
                    summary = response.choices[0].message.content.strip()
                    logger.debug(f"Generated summary for image: {summary[:50]}...")
                    return summary
                    
                except Exception as e:
                    logger.warning(f"Attempt {attempt + 1}/{max_retries} failed for image summary: {e}")
                    if attempt == max_retries - 1:
                        logger.error(f"Failed to generate image summary after {max_retries} attempts: {e}")
                        raise  # Re-raise the exception on final attempt
                    # Wait a bit before retrying
                    import time
                    time.sleep(2 ** attempt)  # Exponential backoff
            
        except Exception as e:
            logger.error(f"Critical error generating image summary: {e}")
            raise  # Re-raise to fail the pipeline
    
    def _insert_image_summary(self, content: str, image_info: Dict[str, any]) -> str:
        """Insert image summary into markdown content.
        
        Args:
            content: Original markdown content
            image_info: Image information with summary
            
        Returns:
            Updated content with summary inserted
        """
        if 'summary' not in image_info:
            return content
        
        # Find the image in content
        image_text = image_info['match_text']
        summary_text = f"\n\n*Image Summary: {image_info['summary']}*\n"
        
        # Insert summary after the image
        updated_content = content.replace(image_text, image_text + summary_text)
        
        return updated_content
    
    def download_remote_images(self, images: List[Dict[str, any]]) -> List[Dict[str, any]]:
        """Download remote images to local storage.
        
        Downloads images from HTTP/HTTPS URLs and saves them locally,
        adding local_path to the image information.
        
        Parameters
        ----------
        images : List[Dict[str, any]]
            List of image information dictionaries
        
        Returns
        -------
        List[Dict[str, any]]
            Updated list with 'local_path' added for downloaded images
        
        Examples
        --------
        >>> processor = ImageProcessor(Path("output"))
        >>> images = [{'url': 'https://example.com/img.png', ...}]
        >>> updated = processor.download_remote_images(images)
        >>> print(updated[0]['local_path'])
        output/images/image_page-1.md_0.png
        
        Notes
        -----
        Determines file extension from Content-Type header.
        Continues processing if individual downloads fail.
        """
        import requests
        
        for idx, image_info in enumerate(images):
            if image_info['url'].startswith('http'):
                try:
                    response = requests.get(image_info['url'], timeout=10)
                    if response.status_code == 200:
                        # Determine file extension
                        ext = '.jpg'  # Default
                        if 'content-type' in response.headers:
                            content_type = response.headers['content-type']
                            if 'png' in content_type:
                                ext = '.png'
                            elif 'gif' in content_type:
                                ext = '.gif'
                        
                        # Create images directory only when we actually need to save an image
                        self.images_dir.mkdir(parents=True, exist_ok=True)
                        
                        # Save locally
                        filename = f"image_{image_info['source_file']}_{idx}{ext}"
                        local_path = self.images_dir / filename
                        
                        with open(local_path, 'wb') as f:
                            f.write(response.content)
                        
                        image_info['local_path'] = str(local_path)
                        logger.debug(f"Downloaded image to {local_path}")
                        
                except Exception as e:
                    logger.error(f"Error downloading image {image_info['url']}: {e}")
        
        return images