import os

def combine_mds(gen_md_dir: str = "swanki-out/gen-md", image_cards_dir: str = "swanki-out/anki-image-cards", output_dir: str = "swanki-out", output_filename: str = "swanki-out.md"):
    """
    Combine all Markdown files from the gen-md directory and interspace them with the corresponding image cards from the anki-image-cards directory into one Markdown file.

    Args:
        gen_md_dir (str): The path to the directory containing the generated text card Markdown files.
        image_cards_dir (str): The path to the directory containing the image card Markdown files.
        output_dir (str): The path to the directory where the combined Markdown file will be saved.
        output_filename (str): The name of the combined Markdown file.
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Initialize a variable to hold the combined content
    combined_content = ""

    # Get a sorted list of generated text card Markdown files
    md_files = sorted(f for f in os.listdir(gen_md_dir) if f.endswith('.md'))

    # Get a sorted list of image card Markdown files
    image_card_files = sorted(f for f in os.listdir(image_cards_dir) if f.endswith('.md'))

    for md_file in md_files:
        # Construct the full path to the generated text card Markdown file
        full_path = os.path.join(gen_md_dir, md_file)

        # Read and concatenate the content of each generated text card Markdown file
        with open(full_path, 'r', encoding='utf-8') as file:
            combined_content += file.read() + '\n\n'

        # Extract the page number from the generated text card Markdown file
        page_number = md_file.split('.')[0].split('-')[1]

        # Find the corresponding image card Markdown files for the current page
        corresponding_image_cards = [f for f in image_card_files if f.startswith(f"page-{page_number}_")]

        # Read and concatenate the content of each corresponding image card Markdown file
        for image_card_file in corresponding_image_cards:
            image_card_path = os.path.join(image_cards_dir, image_card_file)
            with open(image_card_path, 'r', encoding='utf-8') as file:
                combined_content += file.read() + '\n\n'

    # Write the combined content to the new Markdown file
    output_path = os.path.join(output_dir, output_filename)
    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(combined_content)

    print(f"Combined Markdown file created at: {output_path}")