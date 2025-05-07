import os
import subprocess

def convert_pdf_to_markdown(output_dir: str = "swanki-out") -> None:
    """
    This function converts PDF files in the specified directory to markdown files using the mpx-cli tool,
    and outputs the markdown files to a new directory 'md-singles'.
    
    Args:
        output_dir (str): The base output directory where all the files will be stored.
    """
    # Construct paths for PDF and markdown directories
    pdf_folder_path = os.path.join(output_dir, "pdf-singles")
    md_folder_path = os.path.join(output_dir, "md-singles")
    
    # Create a new directory for the markdown files if it doesn't exist
    os.makedirs(md_folder_path, exist_ok=True)
    
    # List all the files in the PDF directory
    pdf_files = [f for f in os.listdir(pdf_folder_path) if f.endswith(".pdf")]

    # Loop over each PDF file
    for pdf_file in pdf_files:
        # Construct the full path to the PDF
        full_pdf_path = os.path.join(pdf_folder_path, pdf_file)

        # Create the markdown file name by replacing the PDF extension with .md
        markdown_file = pdf_file.replace(".pdf", ".md")

        # Construct the full path to the markdown file in the new directory
        full_markdown_path = os.path.join(md_folder_path, markdown_file)

        # Construct the mpx-cli command
        command = f"mpx convert {full_pdf_path} {full_markdown_path}"

        # Execute the command
        subprocess.run(command, shell=True)
        
if __name__ == "__main__":
    pass