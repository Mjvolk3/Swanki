r"""
scripts/schaum_chapter_pack.py
[[scripts.schaum_chapter_pack]]
https://github.com/Mjvolk3/Swanki/tree/main/scripts/schaum_chapter_pack.py

Thin back-compat shim. The chapter-chop + answer-key-concat logic moved into
the library at ``swanki.pdf_prep`` (pure-Python ``pypdf``, CI-covered). This
script forwards its CLI args unchanged so existing ``.sh`` and queue
invocations keep working:

    python scripts/schaum_chapter_pack.py \\
        --source /scratch/alcamoSchaumsOutlineMicrobiology2010_clean.pdf \\
        --chapter-pages 8-18 \\
        --answer-key-pages 328-328 \\
        --output /scratch/alcamo_CH01_packed.pdf

``--answer-key-pages`` may be repeated for a non-contiguous answer key.
"""

from swanki.pdf_prep import main, pack_chapter  # noqa: F401  (re-export)

if __name__ == "__main__":
    main()
