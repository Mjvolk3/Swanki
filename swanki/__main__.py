import argparse
import os
import os.path as osp
import subprocess
from swanki import (
    generate_text_cards,
    recombine_md_files,
    count_tokens_in_md_file,
    combine_mds,
    convert_pdf_to_markdown,
    clean_markdown_files,
    split_pdf_into_pages,
    process_images_summaries,
    generate_image_cards,
)


def main():
    parser = argparse.ArgumentParser(
        description="Swanki: A CLI tool for managing markdown files for Anki card generation."
    )
    parser.add_argument(
        "-f", "--file", help="The path to the PDF file to be processed."
    )
    parser.add_argument(
        "-n",
        "--num-cards",
        type=int,
        help="Number of Anki cards to generate.",
        default=3,
    )
    parser.add_argument(
        "-w",
        "--window-size",
        type=int,
        help="Window size for recombining markdown files.",
        default=2,
    )
    parser.add_argument(
        "-s",
        "--skip",
        type=int,
        help="Number of files to skip in each iteration.",
        default=1,
    )
    args = parser.parse_args()

    # Ensure skip is never larger than window size
    args.skip = min(args.skip, args.window_size)

    if args.file:
        pdf_path = args.file
        split_pdf_into_pages(pdf_path)

        if osp.exists("swanki-out/clean-md-singles"):
            print("Markdown files already cleaned. Skipping.")
        else:
            convert_pdf_to_markdown()
            clean_markdown_files()

        if osp.exists("swanki-out/image-summaries"):
            print("image summaries already generated. Skipping.")
        else:
            source_dir = "swanki-out/clean-md-singles"
            target_dir = "swanki-out/image-summaries"
            process_images_summaries(source_dir, target_dir)

        # Generate image cards
        
        summary_dir = "swanki-out/image-summaries"
        target_dir = "swanki-out/anki-image-cards"
        generate_image_cards(source_dir, summary_dir, target_dir)
    else:
        print("No file provided. Exiting.")
        return

    recombine_md_files(args.window_size)
    recombine_dir = "swanki-out/recombined-md"
    md_files = sorted(f for f in os.listdir(recombine_dir) if f.endswith(".md"))

    # Iterate over the markdown files with the specified skip
    for i in range(0, len(md_files), args.skip):
        md_file_path = os.path.join(recombine_dir, md_files[i])
        # Generate Anki cards for each markdown file based on the skip and window size
        generate_text_cards(md_file_path, args.num_cards)
        print(f"Anki cards generated for {md_file_path}")

    combine_mds(
        gen_md_dir="swanki-out/gen-md",
        image_cards_dir="swanki-out/anki-image-cards",
        output_dir="swanki-out",
        output_filename="combined.md",
    )

    # Clean up inline LaTeX in the combined Markdown file
    combined_file_path = osp.join("swanki-out", "combined.md")
    # replace inline latex marker '\\( ' with '$' and ' \\)' with '$', and handle '\mu' separately
    subprocess.run(
        [
            "sed",
            "-i",
            "s/\\\\\\\\( /$/g; s/ \\\\\\\\)/$/g; s/\\\\mu/\\\\mu/g",
            combined_file_path,
        ]
    )
    print(f"Cleaned up inline LaTeX in {combined_file_path}")


if __name__ == "__main__":
    main()
