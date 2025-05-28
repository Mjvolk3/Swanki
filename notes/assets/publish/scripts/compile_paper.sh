#!/usr/bin/env bash
# Activate env
eval "$(conda shell.bash hook)"
conda activate env-param
# TODO check if it should be at root?
# Export Dendron vault to markdown that can be compiled into document
# Create Bubble Graph - This should be moved into github actions
#dendron visualize --out assets

# export pod
dendron exportPodV2 --podId paper --fname paper --vault Swanki

# Find a and replace asset paths. Prepend `./` to 'assets' so they can be recognized by Pandoc
echo 'Correcting paths for Pandoc'
sed -i '' 's/](assets/](.\/assets/g' *.md

# Pandoc to construct documents
# table of contents option
# pandoc -f gfm --toc -B pod_export/Swanki/paper/title.md pod_export/Swanki/Paper.md -o paper.pdf --reference-doc=reference.docx

# For thesis: pandoc -s notes/export/paper.docx notes/export/paper0.docx -o out.docx --reference-doc=notes/ms_word_ref/paper-reference.docx --citeproc --bibliography notes/bib/bib.bib --metadata csl=notes/bib/nature.csl --toc

# Into notes. This helps maintain  the relative images paths in the notes. (e.g. [](.assets./...))
cd notes

# Set the directory you want to check - This allows for deleting of export and rerun to convice yourself it is working
# CHECK if this can be concatenated below for the hard coded paths.
export_dir="assets/publish/export"

# Check if the directory exists
if [ ! -d "$export_dir" ]; then
    # Create the directory if it does not exist
    mkdir "$export_dir"
fi

echo "PWD:"
echo ${PWD}

# docx_0 - If output looks wrong change/modify paper-reference.docx
pandoc -s assets/publish/Swanki/Paper.md -o assets/publish/export/paper_0.docx --reference-doc=assets/publish/ms_word_ref/paper-reference.docx --citeproc --bibliography assets/publish/bib/bib.bib --metadata csl=assets/publish/bib/nature.csl --metadata title="Paper"


# pdf_0 - Using xelatex with mermaid-filter and header includes (similar to bib_tex_pdf.sh)
pandoc -F mermaid-filter \
  --metadata link-citations=true \
  --metadata title="Paper" \
  -s assets/publish/Swanki/Paper.md \
  -o assets/publish/export/paper_0.pdf \
  --pdf-engine=xelatex \
  --citeproc \
  --bibliography assets/publish/bib/bib.bib \
  --metadata csl=assets/publish/bib/nature.csl \
  -V geometry:"top=2cm, bottom=1.5cm, left=2cm, right=2cm" \
  --include-in-header=assets/publish/tex-templates/header-includes.tex \
  --strip-comments \
  --dpi=600

# pdf_1 - PDF engine wkhtmltopdf
pandoc -s --pdf-engine wkhtmltopdf assets/publish/Swanki/Paper.md -o assets/publish/export/paper_1.pdf --citeproc --bibliography assets/publish/bib/bib.bib --metadata csl=assets/publish/bib/nature.csl -V geometry:"top=2cm, bottom=1.5cm, left=2cm, right=2cm" --strip-comments --metadata title="Paper"

# html
pandoc -s assets/publish/Swanki/Paper.md -o assets/publish/export/paper.html --citeproc --bibliography assets/publish/bib/bib.bib --metadata csl=assets/publish/bib/nature.csl --metadata title="Paper"

# out of notes
cd ..

echo "Paper compiled!"
echo "Generated files:"
echo "  - DOCX: notes/assets/publish/export/paper_0.docx"
echo "  - PDF (xelatex): notes/assets/publish/export/paper_0.pdf"
echo "  - PDF (wkhtmltopdf): notes/assets/publish/export/paper_1.pdf"
echo "  - HTML: notes/assets/publish/export/paper.html"
