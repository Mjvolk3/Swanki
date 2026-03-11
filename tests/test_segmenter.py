"""
tests/test_segmenter.py
[[tests.test_segmenter]]
https://github.com/Mjvolk3/Swanki/tree/main/tests/test_segmenter.py
Test file: N/A

Unit tests for swanki.pipeline.segmenter.
"""

from pathlib import Path

import pytest

from swanki.pipeline.segmenter import (
    build_segment_to_page_map,
    combine_markdown_files,
    split_into_segments,
    write_segment_files,
)


@pytest.fixture()
def md_files(tmp_path: Path) -> list[Path]:
    """Create sample markdown files with varying content."""
    pages = [
        "# Page 1\n\nSome text about topic A.\n\n![img](image1.png)\n",
        "# Page 2\n\nMore text about topic B with $E=mc^2$.\n",
        "# Page 3\n\nFinal page content here.\n",
    ]
    files = []
    for i, content in enumerate(pages):
        p = tmp_path / f"page-{i}.md"
        p.write_text(content)
        files.append(p)
    return files


class TestCombineMarkdownFiles:
    """Tests for combine_markdown_files."""

    def test_combine_preserves_images(self, md_files: list[Path]) -> None:
        """Image refs are preserved in combined output."""
        combined, _ = combine_markdown_files(md_files)
        assert "![img](image1.png)" in combined

    def test_combine_returns_page_offsets(self, md_files: list[Path]) -> None:
        """Offsets correctly track page boundaries."""
        combined, offsets = combine_markdown_files(md_files)
        assert len(offsets) == 3
        assert offsets[0] == 0
        for i, offset in enumerate(offsets):
            page_text = md_files[i].read_text()
            assert combined[offset:].startswith(page_text)


class TestSplitIntoSegments:
    """Tests for split_into_segments."""

    def test_split_respects_newlines(self) -> None:
        """Segments split at newline boundaries."""
        text = "aaaa bbbb cccc\ndddd eeee ffff\ngggg hhhh iiii\njjjj kkkk llll\n"
        segments = split_into_segments(text, target_chars=30)
        assert segments[0][0].endswith("\n")

    def test_split_fallback_to_space(self) -> None:
        """Falls back to space split when no newline in range."""
        text = "word " * 100  # 500 chars, no newlines
        segments = split_into_segments(text, target_chars=50)
        assert len(segments) > 1
        for seg_text, _, _ in segments[:-1]:
            assert seg_text.endswith(" ")

    def test_split_short_content(self) -> None:
        """Content shorter than target_chars yields single segment."""
        text = "Short content."
        segments = split_into_segments(text, target_chars=1000)
        assert len(segments) == 1
        assert segments[0][0] == text

    def test_split_empty_content(self) -> None:
        """Empty input returns empty list."""
        segments = split_into_segments("", target_chars=100)
        assert segments == []

    def test_split_returns_char_ranges(self) -> None:
        """Each tuple has correct (text, start, end)."""
        text = "first segment\nsecond segment\nthird segment\n"
        segments = split_into_segments(text, target_chars=20)
        for seg_text, start, end in segments:
            assert text[start:end] == seg_text

    def test_segment_preserves_equations(self) -> None:
        """LaTeX blocks not split mid-equation."""
        text = (
            "Some text before.\n"
            "$$E = mc^2$$\n"
            "Some text after.\n"
            "More filler text to push past target.\n"
        )
        segments = split_into_segments(text, target_chars=40)
        for seg_text, _, _ in segments:
            if "$$" in seg_text:
                assert "$$E = mc^2$$" in seg_text


class TestWriteSegmentFiles:
    """Tests for write_segment_files."""

    def test_write_segment_files(self, tmp_path: Path) -> None:
        """Creates numbered files in segments/ directory."""
        segments = [
            ("Segment one content", 0, 19),
            ("Segment two content", 19, 38),
        ]
        output_dir = tmp_path / "segments"
        paths = write_segment_files(segments, output_dir)

        assert len(paths) == 2
        assert paths[0].name == "segment-1.md"
        assert paths[1].name == "segment-2.md"
        assert paths[0].read_text() == "Segment one content"
        assert paths[1].read_text() == "Segment two content"
        assert output_dir.exists()


class TestBuildSegmentToPageMap:
    """Tests for build_segment_to_page_map."""

    def test_segment_to_page_map(self) -> None:
        """Mapping correctly identifies overlapping pages."""
        page_offsets = [0, 100, 200]
        segment_ranges = [(0, 150), (150, 300)]
        mapping = build_segment_to_page_map(page_offsets, segment_ranges, 3)

        assert len(mapping) == 2
        assert 0 in mapping[0]
        assert 1 in mapping[0]
        assert 1 in mapping[1]
        assert 2 in mapping[1]

    def test_segment_to_page_map_single_page_segment(self) -> None:
        """Segment within one page maps to just that page."""
        page_offsets = [0, 100, 200]
        segment_ranges = [(110, 190)]
        mapping = build_segment_to_page_map(page_offsets, segment_ranges, 3)

        assert len(mapping) == 1
        assert mapping[0] == [1]
