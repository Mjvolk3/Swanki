"""Image processing module for handling images in markdown files.

This module processes images found in markdown files, generates summaries
for them using AI, and manages image-related operations in the pipeline.
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
    """Handles image extraction, summarization, and processing."""
    
    def __init__(self, output_base: Path, openai_client: Optional[OpenAI] = None):
        """Initialize image processor.
        
        Args:
            output_base: Base directory for all output files
            openai_client: Optional OpenAI client for image summarization
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
        
        Returns:
            List of image information dictionaries
        """
        # Create output directories
        self.image_summaries_dir.mkdir(parents=True, exist_ok=True)
        self.images_dir.mkdir(parents=True, exist_ok=True)
        
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
        
        Args:
            md_path: Path to the markdown file
            
        Returns:
            List of image information dictionaries
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
            if self.openai_client and image_info['url'].startswith('http'):
                summary = self._generate_image_summary(image_info)
                if summary:
                    image_info['summary'] = summary
                    
                    # Save summary to file
                    summary_filename = f"{md_path.stem}_{idx+1}.md"
                    summary_path = self.image_summaries_dir / summary_filename
                    summary_path.write_text(summary, encoding='utf-8')
                    image_info['summary_path'] = summary_path
            
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
        
        Args:
            content: Markdown content
            source_path: Path to the source markdown file
            
        Returns:
            List of image information dictionaries
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
        """Generate a summary for an image using GPT-4V.
        
        Args:
            image_info: Dictionary with image information
            
        Returns:
            Generated summary text, or None if generation failed
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

            response = self.openai_client.chat.completions.create(
                model="gpt-4o",  # or "gpt-4-vision-preview" if using older API
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {"url": image_info['url']}}
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
            logger.error(f"Error generating image summary: {e}")
            return None
    
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
        
        Args:
            images: List of image information dictionaries
            
        Returns:
            Updated list with local paths added
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