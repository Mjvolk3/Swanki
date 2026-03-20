"""
swanki/pipeline/segmenter.py
[[swanki.pipeline.segmenter]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/pipeline/segmenter.py
Test file: tests/test_segmenter.py

Character-based segmentation utilities for splitting markdown content into
uniform-length segments at newline boundaries.
"""

from pathlib import Path


def combine_markdown_files(md_files: list[Path]) -> tuple[str, list[int]]:
    """Concatenate markdown files and track page boundaries.

    Args:
        md_files: Ordered list of per-page markdown files.

    Returns:
        Tuple of (combined_text, page_char_offsets) where
        ``page_char_offsets[i]`` is the starting character index of
        page *i* in the combined text.
    """
    parts: list[str] = []
    offsets: list[int] = []
    pos = 0
    for f in md_files:
        offsets.append(pos)
        text = f.read_text()
        parts.append(text)
        pos += len(text) + 2  # +2 for the "\n\n" separator
    combined = "\n\n".join(parts)
    return combined, offsets


def split_into_segments(text: str, target_chars: int) -> list[tuple[str, int, int]]:
    """Split text into segments of approximately *target_chars* characters.

    Splits at newline boundaries. If no newline is found within the last
    20% of the target window, falls back to the nearest space.

    Args:
        text: The full text to segment.
        target_chars: Target character count per segment.

    Returns:
        List of ``(segment_text, start_char, end_char)`` tuples.
    """
    if not text:
        return []

    segments: list[tuple[str, int, int]] = []
    start = 0
    length = len(text)

    while start < length:
        end = start + target_chars

        if end >= length:
            segments.append((text[start:], start, length))
            break

        # Look backward from end for a newline
        search_start = max(start, end - int(target_chars * 0.2))
        newline_pos = text.rfind("\n", search_start, end)

        if newline_pos > start:
            split_at = newline_pos + 1  # include the newline in current segment
        else:
            # Fallback: nearest space
            space_pos = text.rfind(" ", search_start, end)
            if space_pos > start:
                split_at = space_pos + 1
            else:
                # No good break point — split at target_chars
                split_at = end

        segments.append((text[start:split_at], start, split_at))
        start = split_at

    return segments


def write_segment_files(
    segments: list[tuple[str, int, int]], output_dir: Path
) -> list[Path]:
    """Write segment texts to numbered files.

    Args:
        segments: Output from :func:`split_into_segments`.
        output_dir: Directory to create segment files in (created if needed).

    Returns:
        List of written file paths in segment order.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    for i, (text, _, _) in enumerate(segments, start=1):
        p = output_dir / f"segment-{i}.md"
        p.write_text(text)
        paths.append(p)
    return paths


def build_segment_to_page_map(
    page_offsets: list[int],
    segment_ranges: list[tuple[int, int]],
    total_pages: int,
) -> list[list[int]]:
    """Map each segment to the page indices it overlaps.

    Args:
        page_offsets: Starting character offsets per page (from
            :func:`combine_markdown_files`).
        segment_ranges: ``(start_char, end_char)`` per segment.
        total_pages: Number of pages in the document.

    Returns:
        List where element *i* is the sorted list of page indices
        overlapped by segment *i*.
    """
    # Compute page end boundaries (start of next page, or inf for last)
    page_ends: list[int] = []
    for i in range(total_pages):
        if i + 1 < total_pages:
            page_ends.append(page_offsets[i + 1])
        else:
            page_ends.append(float("inf"))  # type: ignore[arg-type]

    mapping: list[list[int]] = []
    for seg_start, seg_end in segment_ranges:
        pages: list[int] = []
        for page_idx in range(total_pages):
            page_start = page_offsets[page_idx]
            page_end = page_ends[page_idx]
            # Overlap check: segment and page ranges intersect
            if seg_start < page_end and seg_end > page_start:
                pages.append(page_idx)
        mapping.append(pages)
    return mapping
