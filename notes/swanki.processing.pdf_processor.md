---
id: srtjn64ruwqfhcb058qs39t
title: Pdf_processor
desc: ''
updated: 1772137857891
created: 1772137857891
---

## 2026.02.26 - Add qpdf fallback for malformed PDFs

PyPDF2 can fail on certain malformed or non-standard PDFs. The split method now catches PyPDF2 errors and falls back to a `_split_pdf_qpdf` helper that shells out to `qpdf` for page-by-page extraction. This keeps the pipeline from breaking on real-world PDFs that PyPDF2 cannot parse.

- `split_pdf` catches exceptions from PyPDF2 and delegates to `_split_pdf_qpdf`
- `_split_pdf_qpdf` uses `subprocess.run` with qpdf, treating exit codes 0 and 3 (warnings) as success
- Raises `ValueError` if qpdf is not installed or returns a hard error
- Removed redundant inline comments and cleaned up whitespace
