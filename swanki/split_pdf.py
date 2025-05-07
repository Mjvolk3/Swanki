import os
from PyPDF2 import PdfReader, PdfWriter


def split_pdf_into_pages(pdf_path: str, output_dir: str = "swanki-out") -> None:
    # Construct the full output directory path
    pdf_singles_dir = os.path.join(output_dir, "pdf-singles")
    
    # Ensure the output directory exists
    if not os.path.exists(pdf_singles_dir):
        os.makedirs(pdf_singles_dir)

    # Open the source PDF
    reader = PdfReader(pdf_path)

    # Loop through each page in the PDF
    for i, page in enumerate(reader.pages, start=1):
        writer = PdfWriter()
        writer.add_page(page)

        # Construct output filename
        output_filename = os.path.join(pdf_singles_dir, f"page-{i}.pdf")

        # Write out the single page PDF
        with open(output_filename, "wb") as output_pdf:
            writer.write(output_pdf)

        print(f"Created: {output_filename}")