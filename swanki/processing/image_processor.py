"""
swanki/processing/image_processor.py
[[swanki.processing.image_processor]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/processing/image_processor.py
Test file: tests/test_image_processor.py

Image extraction, AI summarization, and processing for markdown files.
"""

from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, unquote, urlparse

from ..llm.agents import text_agent

logger = logging.getLogger(__name__)

ImageInfo = dict[str, Any]


class ImageProcessor:
    """Extracts images from markdown, generates AI summaries, and manages files.

    Args:
        output_base: Base directory for all output files.
        model: pydantic-ai model string for image summarization.
    """

    def __init__(self, output_base: Path, model: str = "openai:gpt-4o") -> None:
        """Initialize image processor.

        Args:
            output_base: Base directory for all output files. Will create
                subdirectories for image summaries and downloaded images.
            model: pydantic-ai model string (e.g. ``"openai:gpt-4o"``).
        """
        self.output_base = output_base
        self.clean_md_singles_dir = output_base / "clean-md-singles"
        self.image_summaries_dir = output_base / "image-summaries"
        self.images_dir = output_base / "images"
        self.model = model

    def process_all_images(self) -> list[ImageInfo]:
        """Process all images found in cleaned markdown files.

        Returns:
            List of image info dicts with keys: url, alt_text, context,
            summary, source_file.
        """
        self.image_summaries_dir.mkdir(parents=True, exist_ok=True)

        md_files = sorted(self.clean_md_singles_dir.glob("*.md"))

        all_images: list[ImageInfo] = []
        for md_file in md_files:
            images = self.process_images_in_file(md_file)
            all_images.extend(images)

        logger.info(f"Processed {len(all_images)} images total")
        return all_images

    def process_images_in_file(self, md_path: Path) -> list[ImageInfo]:
        """Process all images in a single markdown file.

        Args:
            md_path: Path to the markdown file to process.

        Returns:
            List of processed image information dictionaries.
        """
        if not md_path.exists():
            logger.error(f"Markdown file not found: {md_path}")
            return []

        content = md_path.read_text(encoding="utf-8")

        images = self._extract_images_from_markdown(content, md_path)

        processed_images: list[ImageInfo] = []
        for idx, image_info in enumerate(images):
            if self.model:
                summary = self._generate_image_summary(image_info)
                if summary:
                    image_info["summary"] = summary

                    summary_filename = f"{md_path.stem}_{idx + 1}.md"
                    summary_path = self.image_summaries_dir / summary_filename
                    summary_path.write_text(summary, encoding="utf-8")
                    image_info["summary_path"] = summary_path
                else:
                    error_msg = f"No summary generated for image: {image_info['url']}"
                    logger.error(error_msg)
                    raise RuntimeError(error_msg)

            if "summary" in image_info:
                content = self._insert_image_summary(content, image_info)

            processed_images.append(image_info)

        if any("summary" in img for img in processed_images):
            updated_path = (
                self.image_summaries_dir / f"{md_path.stem}_with_summaries.md"
            )
            updated_path.write_text(content, encoding="utf-8")

        return processed_images

    def _extract_images_from_markdown(
        self, content: str, source_path: Path
    ) -> list[ImageInfo]:
        """Extract all images from markdown content.

        Args:
            content: Markdown content to parse.
            source_path: Path to the source markdown file.

        Returns:
            List of image info dicts with metadata.
        """
        images: list[ImageInfo] = []

        image_pattern = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")

        for match in image_pattern.finditer(content):
            alt_text = match.group(1)
            url = match.group(2)

            cleaned_url = self._clean_image_url(url)

            start = max(0, match.start() - 200)
            end = min(len(content), match.end() + 200)
            context = content[start:end].strip()

            image_info: ImageInfo = {
                "alt_text": alt_text,
                "url": cleaned_url,
                "original_url": url,
                "context": context,
                "source_file": source_path.name,
                "position": match.start(),
                "match_text": match.group(0),
            }

            images.append(image_info)

        logger.debug(f"Found {len(images)} images in {source_path.name}")
        return images

    def _clean_image_url(self, url: str) -> str:
        """Clean and normalize image URLs.

        Args:
            url: Original URL string.

        Returns:
            Cleaned URL.
        """
        cleaned = unquote(url.replace("\\", "").replace("\n", "").strip())
        return cleaned

    def _generate_image_summary(self, image_info: ImageInfo) -> str | None:
        """Generate a summary for an image using vision model via pydantic-ai.

        Args:
            image_info: Dictionary containing image URL and context.

        Returns:
            Generated summary text (2-4 sentences), or None if failed.
        """
        from pydantic_ai import BinaryContent, ImageUrl

        prompt = f"""Please analyze this image and provide a comprehensive summary.

Context around the image: {image_info["context"]}

Describe:
1. What the image shows (diagrams, graphs, equations, etc.)
2. Key information or data presented
3. How it relates to the surrounding text
4. Any important details that would help understand the content

Keep the summary concise but informative (2-4 sentences)."""

        image_url: str = image_info["url"]
        image_content: BinaryContent | ImageUrl

        if not image_url.startswith("http"):
            # Local image — read bytes and use BinaryContent
            source_dir = self.clean_md_singles_dir
            possible_paths = [
                source_dir / image_url,
                source_dir.parent / image_url,
                self.output_base / image_url,
                Path(image_url),
            ]

            image_path = None
            for path in possible_paths:
                if path.exists() and path.is_file():
                    image_path = path
                    break

            if not image_path:
                logger.error(f"Local image not found: {image_url}")
                return None

            mime_type = (
                "image/png" if image_path.suffix.lower() == ".png" else "image/jpeg"
            )
            image_content = BinaryContent(
                data=image_path.read_bytes(), media_type=mime_type
            )
        else:
            # Remote image — check dimensions and potentially resize
            max_dimension = 2000
            parsed = urlparse(image_url)
            params = parse_qs(parsed.query)
            img_h = int(params.get("height", ["0"])[0])
            img_w = int(params.get("width", ["0"])[0])

            if img_h > max_dimension or img_w > max_dimension:
                import io

                import requests
                from PIL import Image as PILImage

                logger.info(
                    f"Remote image too large ({img_w}x{img_h}), downloading and resizing"
                )
                resp = requests.get(image_url, timeout=60)
                resp.raise_for_status()
                opened = PILImage.open(io.BytesIO(resp.content))
                scale = max_dimension / max(opened.size)
                new_size = (int(opened.size[0] * scale), int(opened.size[1] * scale))
                resized = opened.resize(new_size, PILImage.Resampling.LANCZOS)
                logger.info(f"Resized to {resized.size[0]}x{resized.size[1]}")
                buf = io.BytesIO()
                resized.convert("RGB").save(buf, format="JPEG", quality=85)
                image_content = BinaryContent(
                    data=buf.getvalue(), media_type="image/jpeg"
                )
            else:
                image_content = ImageUrl(url=image_url)

        result = text_agent.run_sync(
            [prompt, image_content],
            model=self.model,
            model_settings={"max_tokens": 1024, "temperature": 0.3},
        )
        summary: str = result.output.strip()
        logger.debug(f"Generated summary for image: {summary[:50]}...")
        return summary

    def _insert_image_summary(self, content: str, image_info: ImageInfo) -> str:
        """Insert image summary into markdown content after the image.

        Args:
            content: Original markdown content.
            image_info: Image information with summary.

        Returns:
            Updated content with summary inserted.
        """
        if "summary" not in image_info:
            return content

        image_text: str = image_info["match_text"]
        summary_text = f"\n\n*Image Summary: {image_info['summary']}*\n"

        updated_content = content.replace(image_text, image_text + summary_text)

        return updated_content

    def download_remote_images(self, images: list[ImageInfo]) -> list[ImageInfo]:
        """Download remote images to local storage.

        Args:
            images: List of image information dictionaries.

        Returns:
            Updated list with ``local_path`` added for downloaded images.
        """
        import requests

        for idx, image_info in enumerate(images):
            url: str = image_info["url"]
            if url.startswith("http"):
                try:
                    response = requests.get(url, timeout=10)
                    if response.status_code == 200:
                        ext = ".jpg"
                        if "content-type" in response.headers:
                            content_type = response.headers["content-type"]
                            if "png" in content_type:
                                ext = ".png"
                            elif "gif" in content_type:
                                ext = ".gif"

                        self.images_dir.mkdir(parents=True, exist_ok=True)

                        filename = f"image_{image_info['source_file']}_{idx}{ext}"
                        local_path = self.images_dir / filename

                        with open(local_path, "wb") as f:
                            f.write(response.content)

                        image_info["local_path"] = str(local_path)
                        logger.debug(f"Downloaded image to {local_path}")

                except Exception as e:
                    logger.error(f"Error downloading image {url}: {e}")

        return images
