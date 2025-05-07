# swanki/generate_reading_transcript.py
import os
import re


def generate_reading_transcript_input(
    clean_md_dir: str, image_summaries_dir: str, output_file: str
):
    """
    Generates input for verbatim reading transcript by cleaning markdown files
    of non-readable elements and preparing text for audio generation.

    Args:
        clean_md_dir (str): Directory containing cleaned markdown files
        image_summaries_dir (str): Directory containing image summaries
        output_file (str): Path to save the generated transcript input
    """
    md_files = sorted([f for f in os.listdir(clean_md_dir) if f.endswith(".md")])
    transcript_input = ""

    for md_file in md_files:
        md_file_path = os.path.join(clean_md_dir, md_file)
        with open(md_file_path, "r", encoding="utf-8") as file:
            md_content = file.read()

        # Find all image URLs in the Markdown content
        image_patterns = re.findall(
            r"!\[\]\((https://cdn\.mathpix\.com/[^)]+)\)", md_content
        )

        # Process each image reference
        for image_url in image_patterns:
            # Find the corresponding image summary file
            page_number = md_file.split(".")[0].split("-")[1]
            image_index = image_patterns.index(image_url) + 1
            summary_file = f"page-{page_number}_{image_index}.md"
            summary_path = os.path.join(image_summaries_dir, summary_file)

            if os.path.exists(summary_path):
                with open(summary_path, "r", encoding="utf-8") as file:
                    summary_content = file.read()

                # Replace image markdown with figure description text
                replacement = f"[Figure {image_index}: {summary_content.strip()}]"
                md_content = md_content.replace(f"![](${image_url})", replacement)

        # Process LaTeX equations for verbal reading
        # Inline equations
        md_content = re.sub(
            r"\$([^$]+)\$", lambda m: f"[Equation: {m.group(1)}]", md_content
        )

        # Display equations
        md_content = re.sub(
            r"\$\$(.*?)\$\$",
            lambda m: f"[Equation: {m.group(1)}]",
            md_content,
            flags=re.DOTALL,
        )

        # Clean other markdown elements
        md_content = re.sub(r"\*\*(.*?)\*\*", r"\1", md_content)  # Remove bold
        md_content = re.sub(r"\*(.*?)\*", r"\1", md_content)  # Remove italic
        md_content = re.sub(
            r"#{1,6}\s+(.*)", r"\1.", md_content
        )  # Convert headers to sentences

        transcript_input += md_content + "\n\n"

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(transcript_input)

    return output_file


def clean_reading_transcript(input_file: str, output_file: str):
    """
    Cleans the reading transcript to make it more suitable for TTS by removing
    superfluous academic formatting and references.

    Args:
        input_file (str): Path to the input transcript file
        output_file (str): Path to save the cleaned transcript
    """
    with open(input_file, "r", encoding="utf-8") as file:
        content = file.read()

    # Remove superscripted references and citation brackets
    content = re.sub(r"\{\s*\^\s*\d+(?:,\s*\d+)*\s*\}", "", content)
    content = re.sub(r"\{\s*\^[^}]*\}", "", content)

    # Remove citation references like [Equation: { }^{20}]
    content = re.sub(r"\[Equation: \{\s*\}(?:\^\{\d+\})?\]", "", content)

    # Clean up author information sections
    content = re.sub(r"\{\s*\d+\]\s*[^,.]+?,[^,.]+?\.", "", content)

    # Remove email addresses and corresponding text
    content = re.sub(r"\\boxtimes.*?;.*?@.*?\.(?:fr|com|org|edu)", "", content)
    content = re.sub(r"e-mail:.*?@.*?\.(?:fr|com|org|edu)", "", content)

    # Remove document metadata sections
    content = re.sub(r"\\footnotetext\{[^}]*\}", "", content)
    content = re.sub(r"\\title\{[^}]*\}", "", content)
    content = re.sub(r"Received:.*?Published online:.*?", "", content, flags=re.DOTALL)

    # Remove remaining markdown artifacts
    content = re.sub(
        r"\[(.*?)\]\(.*?\)", r"\1", content
    )  # Remove links but keep link text
    content = re.sub(
        r"^\s*-\s+", "", content, flags=re.MULTILINE
    )  # Remove list markers

    # Remove excessive whitespace caused by deletions
    content = re.sub(r"\n{3,}", "\n\n", content)  # Reduce multiple newlines
    content = re.sub(r"\s{2,}", " ", content)  # Reduce multiple spaces

    # Process equations without adding "The equation" prefix
    content = re.sub(r"\[Equation: (.*?)\]", r"\1", content)

    # Clean up figure numbers for more natural speech
    content = re.sub(
        r"\[Figure (\d+): (.*?)\]",
        lambda m: f"Figure {m.group(1)}. {m.group(2)}",
        content,
    )

    # Remove 'Fig. X |' references
    content = re.sub(r"Fig\.\s*\d+\s*\\mid", "", content)

    # Clean up bibliographic references
    content = re.sub(r"\{\\.*?\}", "", content)  # Remove LaTeX commands

    # Remove section header symbols
    content = re.sub(r"\\section\*\{(.*?)\}", r"\1", content)

    # Fix common LaTeX symbols for reading
    content = re.sub(r"\\sim", "approximately", content)
    content = re.sub(r"\\times", "times", content)
    content = re.sub(r"\\mathrm", "", content)
    content = re.sub(r"\\log", "log", content)

    content = content.strip()

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(content)
