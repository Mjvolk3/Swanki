import os
import re


def combine_mds(
    text_cards_dir: str,
    image_cards_dir: str,
    output_dir: str,
    output_filename: str = "swanki-out.md",
    citation_key: str = None,
):
    """
    Combine all generated Anki cards from the text cards directory and image cards directory
    into one Markdown file, in the order of text cards followed by image cards for each page.

    Args:
        text_cards_dir (str): The path to the directory containing the text-generated card Markdown files.
        image_cards_dir (str): The path to the directory containing the image-generated card Markdown files.
        output_dir (str): The path to the directory where the combined Markdown file will be saved.
        output_filename (str): The name of the combined Markdown file.
        citation_key (str): Optional citation key to prefix questions.
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Add citation key if provided
    citation_prefix = f"{citation_key}: " if citation_key else ""

    # Initialize a variable to hold the combined content
    combined_content = ""

    # Get a sorted list of text-generated card Markdown files
    text_card_files = sorted(f for f in os.listdir(text_cards_dir) if f.endswith(".md"))

    for text_card_file in text_card_files:
        text_card_path = os.path.join(text_cards_dir, text_card_file)

        # Extract the page number from the text card filename
        page_number = text_card_file.split(".")[0].split("-")[1]

        # Read content of the text-generated card Markdown file
        with open(text_card_path, "r", encoding="utf-8") as file:
            content = file.read()

            # Add citation key to each H2 heading if not already present
            if citation_key:
                content = re.sub(
                    r"(## )((?!" + re.escape(citation_prefix) + r").*?)(\n)",
                    r"\1" + citation_prefix + r"\2\3",
                    content,
                )

            combined_content += content + "\n\n"

        # Find the corresponding image-generated card Markdown files for the current page
        os.makedirs(image_cards_dir, exist_ok=True)
        image_card_files = sorted(
            f
            for f in os.listdir(image_cards_dir)
            if f.startswith(f"page-{page_number}_") and f.endswith(".md")
        )

        # Read and concatenate the content of each corresponding image-generated card Markdown file
        for image_card_file in image_card_files:
            image_card_path = os.path.join(image_cards_dir, image_card_file)
            with open(image_card_path, "r", encoding="utf-8") as file:
                content = file.read()

                # Add citation key to each H2 heading if not already present
                if citation_key:
                    content = re.sub(
                        r"(## )((?!" + re.escape(citation_prefix) + r").*?)(\n)",
                        r"\1" + citation_prefix + r"\2\3",
                        content,
                    )

                combined_content += content + "\n\n"

    # Write the combined content to the new Markdown file
    output_path = os.path.join(output_dir, output_filename)
    with open(output_path, "w", encoding="utf-8") as output_file:
        output_file.write(combined_content)

    print(f"Combined Markdown file created at: {output_path}")
