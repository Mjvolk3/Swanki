# swanki/__main__.py
import argparse
import os
import os.path as osp
from pathlib import Path
import re
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
    generate_transcript_input,
    generate_transcript,
    clean_transcript,
    generate_audio_from_transcript,
    generate_reading_transcript_input,
    clean_reading_transcript,
    generate_complementary_audio_transcript_plain_card,
    generate_complementary_audio_transcript_image_card,
    generate_audio_from_transcripts,
    enrich_gen_md,
    enrich_image_cards,
)


def get_file_content(file_path: str) -> str:
    """
    Returns the content of a file if it exists, otherwise returns an empty string.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:  # Ensure UTF-8 encoding
            return file.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return ""


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
        help="Number of Anki cards to generate per page (ppg).",
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
    parser.add_argument(
        "-o",
        "--output-dir",
        help="Directory where output files will be stored.",
        default="swanki-out",
    )
    # Add audio generation options
    parser.add_argument(
        "--audio-summary",
        action="store_true",
        help="Generate summarized audio transcript (explanatory style)",
    )
    parser.add_argument(
        "--audio-reading",
        action="store_true",
        help="Generate verbatim reading audio (audiobook style)",
    )
    parser.add_argument(
        "--complementary-audio",
        action="store_true",
        help="Generate complementary audio for cards (audio versions of questions and answers)",
    )
    parser.add_argument(
        "--citation-key",
        help="Citation key to prefix cards and audio (e.g., @authorTitleYear)",
        default=None,
    )
    args = parser.parse_args()

    # Ensure skip is never larger than window size
    args.skip = min(args.skip, args.window_size)

    # Ensure output directory exists
    os.makedirs(args.output_dir, exist_ok=True)

    if args.file:
        pdf_path = args.file
        output_dir = args.output_dir

        # Update all path references with the output_dir
        split_pdf_into_pages(pdf_path, output_dir=output_dir)

        clean_md_singles_dir = osp.join(output_dir, "clean-md-singles")
        if osp.exists(clean_md_singles_dir):
            print("Markdown files already cleaned. Skipping.")
        else:
            convert_pdf_to_markdown(output_dir=output_dir)
            clean_markdown_files(output_dir=output_dir)

        successful_summaries = []
        image_summaries_dir = osp.join(output_dir, "image-summaries")
        if osp.exists(image_summaries_dir):
            print("Image summaries already generated. Skipping.")
        else:
            source_dir = clean_md_singles_dir
            target_dir = image_summaries_dir
            successful_summaries = process_images_summaries(source_dir, target_dir)

        # Check if all image summaries were generated successfully
        source_dir = clean_md_singles_dir
        md_files = sorted([f for f in os.listdir(source_dir) if f.endswith(".md")])
        total_images = sum(
            len(
                re.findall(
                    r"!\[\]\((https://cdn.mathpix.com/[^)]+)\)",
                    get_file_content(osp.join(source_dir, md_file)),
                )
            )
            for md_file in md_files
        )
        if len(successful_summaries) != total_images:
            print("Not all image summaries were generated successfully. Exiting.")
            return

        # Generate image cards only for the successfully generated summaries
        summary_dir = image_summaries_dir
        target_dir = osp.join(output_dir, "anki-image-cards")
        if successful_summaries:
            # Group summaries by md_file
            summaries_by_md_file = {}
            for image_url, md_file, summary_file in successful_summaries:
                if md_file not in summaries_by_md_file:
                    summaries_by_md_file[md_file] = []
                summaries_by_md_file[md_file].append((image_url, summary_file))

            for md_file, summaries in summaries_by_md_file.items():
                image_urls = [summary[0] for summary in summaries]
                generate_image_cards(
                    source_dir, summary_dir, target_dir, image_urls, md_file
                )
        else:
            print("No successful image summaries found. Skipping card generation.")

        # Generate text cards from the cleaned Markdown files
        clean_md_dir = clean_md_singles_dir
        for md_file in os.listdir(clean_md_dir):
            if md_file.endswith(".md"):
                md_file_path = os.path.join(clean_md_dir, md_file)
                generate_text_cards(
                    md_file_path, num_cards=args.num_cards, output_dir=output_dir
                )
        gen_md_dir = osp.join(output_dir, "gen-md")
        image_cards_dir = osp.join(output_dir, "anki-image-cards")
        if args.complementary_audio:
            print("Generating complementary audio for cards...")

            # 1. Generate transcripts for plain/text cards
            gen_md_dir = osp.join(output_dir, "gen-md")
            transcript_dir = osp.join(
                output_dir, "gen-md-complementary-audio-transcript"
            )
            os.makedirs(transcript_dir, exist_ok=True)

            print("Generating transcripts for text cards...")
            for md_file in os.listdir(gen_md_dir):
                if md_file.endswith(".md"):
                    md_path = osp.join(gen_md_dir, md_file)
                    generate_complementary_audio_transcript_plain_card(
                        md_path, transcript_dir, args.citation_key
                    )

            # 2. Generate transcripts for image cards
            image_cards_dir = osp.join(output_dir, "anki-image-cards")
            image_transcript_dir = osp.join(
                output_dir, "anki-image-cards-complementary-audio-transcript"
            )
            os.makedirs(image_transcript_dir, exist_ok=True)

            print("Generating transcripts for image cards...")
            for md_file in os.listdir(image_cards_dir):
                if md_file.endswith(".md"):
                    md_path = osp.join(image_cards_dir, md_file)
                    generate_complementary_audio_transcript_image_card(
                        md_path,
                        image_transcript_dir,
                        osp.join(output_dir, "image-summaries"),
                        args.citation_key,
                    )

            # 3. Generate audio from transcripts for text cards
            audio_dir = osp.join(output_dir, "gen-md-complementary-audio")
            os.makedirs(audio_dir, exist_ok=True)

            print("Generating audio for text card transcripts...")
            try:
                generate_audio_from_transcripts(
                    transcript_dir, audio_dir, None
                )  # Use default voice ID
            except Exception as e:
                print(f"Error generating audio for text cards: {e}")

            # 4. Generate audio from transcripts for image cards
            image_audio_dir = osp.join(
                output_dir, "anki-image-cards-complementary-audio"
            )
            os.makedirs(image_audio_dir, exist_ok=True)

            print("Generating audio for image card transcripts...")
            try:
                generate_audio_from_transcripts(
                    image_transcript_dir, image_audio_dir, None
                )  # Use default voice ID
            except Exception as e:
                print(f"Error generating audio for image cards: {e}")

            # 5. Enrich text cards with audio links
            enriched_gen_md_dir = osp.join(
                output_dir, "gen-md-with-complementary-audio"
            )
            os.makedirs(enriched_gen_md_dir, exist_ok=True)

            print("Enriching text cards with audio links...")
            enrich_gen_md(Path(gen_md_dir), Path(audio_dir), Path(enriched_gen_md_dir))

            # 6. Enrich image cards with audio links
            enriched_image_cards_dir = osp.join(
                output_dir, "anki-image-cards-with-complementary-audio"
            )
            os.makedirs(enriched_image_cards_dir, exist_ok=True)

            print("Enriching image cards with audio links...")
            enrich_image_cards(
                Path(image_cards_dir),
                Path(image_audio_dir),
                Path(enriched_image_cards_dir),
            )

            # 7. Use the enriched card directories for the final combine step
            gen_md_dir = enriched_gen_md_dir
            image_cards_dir = enriched_image_cards_dir

        # Combine the generated Markdown files
        combine_mds(
            text_cards_dir=gen_md_dir,  # Use the variable, not hardcoded path
            image_cards_dir=image_cards_dir,  # Use the variable, not hardcoded path
            output_dir=output_dir,
            output_filename="swanki-out.md",
            citation_key=args.citation_key,
        )

        # Clean up inline LaTeX in the combined Markdown file
        combined_file_path = osp.join(output_dir, "combined.md")
        subprocess.run(
            [
                "sed",
                "-i",
                "s/\\\\\\\\( /$/g; s/ \\\\\\\\)/$/g; s/\\\\mu/\\\\mu/g",
                combined_file_path,
            ]
        )
        print(f"Cleaned up inline LaTeX in {combined_file_path}")

        # Handle audio generation based on flags
        clean_md_dir = clean_md_singles_dir

        # Generate summarized audio if requested
        if args.audio_summary:
            print("Generating summarized audio transcript...")

            # Generate the transcript input by combining clean-md-singles and image-summaries
            transcript_input_file = osp.join(output_dir, "transcript-input-summary.md")
            generate_transcript_input(
                clean_md_dir, image_summaries_dir, transcript_input_file
            )

            # Generate the transcript using the OpenAI API
            transcript_output_file = osp.join(
                output_dir, "transcript-output-summary.md"
            )
            generate_transcript(transcript_input_file, transcript_output_file)
            print(f"Summary transcript generated and saved to {transcript_output_file}")

            # Clean and refine the generated transcript
            clean_output_file = osp.join(output_dir, "transcript-clean-summary.md")
            clean_transcript(transcript_output_file, clean_output_file)
            print(f"Clean summary transcript saved to {clean_output_file}")

            # Generate audio from the cleaned transcript
            transcript_path = Path(clean_output_file)
            audio_output_dir = Path(osp.join(output_dir, "audio-summary"))
            audio_output_dir.mkdir(exist_ok=True)

            try:
                audio_path = generate_audio_from_transcript(
                    transcript_path, audio_output_dir
                )
                print(f"Summary audio generated successfully at: {audio_path}")
            except Exception as e:
                print(f"Failed to generate summary audio: {e}")

        # Generate verbatim reading audio if requested
        if args.audio_reading:
            print("Generating verbatim reading audio transcript...")

            # Generate the reading transcript input
            transcript_input_file = osp.join(output_dir, "transcript-input-reading.md")
            generate_reading_transcript_input(
                clean_md_dir, image_summaries_dir, transcript_input_file
            )

            # Clean the reading transcript for TTS
            clean_output_file = osp.join(output_dir, "transcript-clean-reading.md")
            clean_reading_transcript(transcript_input_file, clean_output_file)
            print(f"Clean reading transcript saved to {clean_output_file}")

            # Generate audio from the cleaned reading transcript
            transcript_path = Path(clean_output_file)
            audio_output_dir = Path(osp.join(output_dir, "audio-reading"))
            audio_output_dir.mkdir(exist_ok=True)

            try:
                audio_path = generate_audio_from_transcript(
                    transcript_path, audio_output_dir
                )
                print(f"Reading audio generated successfully at: {audio_path}")
            except Exception as e:
                print(f"Failed to generate reading audio: {e}")

        # Maintain backward compatibility if neither audio flag is set
        if not (args.audio_summary or args.audio_reading):
            print("No audio generation requested. Skipping audio generation.")

    else:
        print("No file provided. Exiting.")
        return


if __name__ == "__main__":
    main()
