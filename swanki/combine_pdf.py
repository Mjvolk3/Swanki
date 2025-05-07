import argparse
import os
from typing import List
from PyPDF2 import PdfReader, PdfWriter


def combine_pdfs(input_files: List[str], output_file: str) -> None:
    """Combine multiple PDF files into a single PDF.
    
    Args:
        input_files: List of paths to input PDF files
        output_file: Path where the combined PDF will be saved
    """
    writer = PdfWriter()

    for pdf_file in input_files:
        reader = PdfReader(pdf_file)
        for page in reader.pages:
            writer.add_page(page)

    with open(output_file, "wb") as out_pdf:
        writer.write(out_pdf)
        
    print(f"Combined PDF saved to {output_file}")


def main():
    parser = argparse.ArgumentParser(description="Combine multiple PDF files.")
    parser.add_argument(
        "-i", 
        "--input_files", 
        nargs="+", 
        required=True,
        help="List of input PDF files to combine"
    )
    parser.add_argument(
        "-o",
        "--output",
        required=True,
        help="Output PDF file path"
    )

    args = parser.parse_args()

    # Validate input files exist
    for file in args.input_files:
        if not os.path.exists(file):
            print(f"Error: The file {file} does not exist.")
            return

    combine_pdfs(args.input_files, args.output)


if __name__ == "__main__":
    main()