"""
swanki/presentation/renderer.py
[[swanki.presentation.renderer]]
https://github.com/Mjvolk3/swanki/tree/main/swanki/presentation/renderer.py
Test file: tests/swanki/presentation/test_renderer.py

Render a Presentation model to pandoc markdown and then to Reveal.js HTML.
"""

import subprocess
from pathlib import Path

from swanki.presentation.models import Presentation, Slide


class PresentationRenderer:
    """Render a Presentation to Reveal.js HTML via pandoc.

    Args:
        output_dir: Directory for slides.md and presentation.html output.
    """

    def __init__(self, output_dir: Path) -> None:
        """Initialize with output directory."""
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _slide_to_markdown(
        self, slide: Slide, figure_paths: dict[str, Path], is_first: bool
    ) -> str:
        """Convert a single Slide to pandoc markdown."""
        parts: list[str] = []

        # Slide header
        if is_first and slide.layout == "title":
            # Title slide handled by YAML front matter
            if slide.content:
                parts.append(slide.content)
        else:
            parts.append(f"## {slide.title}")
            parts.append("")
            if slide.content:
                parts.append(slide.content)

        # Embed figures
        for fig in slide.figures:
            fig_path = figure_paths.get(fig.label)
            if fig_path is not None:
                rel_path = fig_path.name
                parts.append("")
                parts.append(f"![{fig.caption}](figures/{rel_path}){{width=80%}}")

        # Embed mermaid diagrams
        for diagram in slide.mermaid_diagrams:
            parts.append("")
            parts.append("```{.mermaid}")
            parts.append(diagram.code)
            parts.append("```")
            if diagram.caption:
                parts.append("")
                parts.append(f"*{diagram.caption}*")

        # Speaker notes
        if slide.speaker_notes:
            parts.append("")
            parts.append("::: notes")
            parts.append(slide.speaker_notes)
            parts.append(":::")

        return "\n".join(parts)

    def generate_markdown(
        self, presentation: Presentation, figure_paths: dict[str, Path]
    ) -> Path:
        """Generate pandoc-flavored markdown with YAML front matter.

        Args:
            presentation: Structured presentation data.
            figure_paths: Mapping from figure label to PNG path.

        Returns:
            Path to the generated slides.md file.
        """
        # YAML front matter
        authors_str = ", ".join(presentation.authors)
        front_matter = [
            "---",
            f'title: "{presentation.title}"',
        ]
        if presentation.subtitle:
            front_matter.append(f'subtitle: "{presentation.subtitle}"')
        front_matter.extend(
            [
                f'author: "{authors_str}"',
                f'date: "{presentation.date}"',
                "revealjs-url: https://unpkg.com/reveal.js@5.1.0",
                "theme: white",
                "slideNumber: true",
                "transition: slide",
                "---",
            ]
        )

        sections: list[str] = ["\n".join(front_matter)]

        for i, slide in enumerate(presentation.slides):
            md = self._slide_to_markdown(slide, figure_paths, is_first=(i == 0))
            sections.append(md)

        content = "\n\n---\n\n".join(sections)
        md_path = self.output_dir / "slides.md"
        md_path.write_text(content, encoding="utf-8")
        return md_path

    def render_html(self, md_path: Path) -> Path:
        """Render pandoc markdown to Reveal.js HTML.

        Args:
            md_path: Path to slides.md input.

        Returns:
            Path to the generated presentation.html file.
        """
        html_path = self.output_dir / "presentation.html"

        cmd = [
            "pandoc",
            "-F",
            "mermaid-filter",
            str(md_path),
            "-f",
            "markdown-implicit_figures",
            "-t",
            "revealjs",
            "--standalone",
            "--katex",
            f"--resource-path={self.output_dir}",
            "-o",
            str(html_path),
        ]

        # Use CDN for reveal.js (embedded data URIs break in Chrome file://)
        import os

        env = os.environ.copy()
        env["MERMAID_FILTER_SCALE"] = "4"
        env["MERMAID_FILTER_WIDTH"] = "2400"
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            env=env,
        )
        if result.returncode != 0:
            msg = f"pandoc failed: {result.stderr}"
            raise RuntimeError(msg)

        # Inject quarto-ext/pointer plugin before </body>
        pointer_css = self.output_dir / "pointer.css"
        pointer_js = self.output_dir / "pointer.js"
        pointer_script = ""
        if pointer_js.exists():
            js_content = pointer_js.read_text(encoding="utf-8")
            css_content = (
                pointer_css.read_text(encoding="utf-8") if pointer_css.exists() else ""
            )
            pointer_script = f"""
<style>{css_content}</style>
<script>{js_content}</script>
<script>
Reveal.registerPlugin(RevealPointer);
</script>
"""
        html_content = html_path.read_text(encoding="utf-8")
        html_content = html_content.replace("</body>", pointer_script + "</body>")
        html_path.write_text(html_content, encoding="utf-8")

        return html_path

    def render(self, presentation: Presentation, figure_paths: dict[str, Path]) -> Path:
        """Full render pipeline: markdown then HTML.

        Args:
            presentation: Structured presentation data.
            figure_paths: Mapping from figure label to PNG path.

        Returns:
            Path to the generated presentation.html.
        """
        md_path = self.generate_markdown(presentation, figure_paths)
        return self.render_html(md_path)
