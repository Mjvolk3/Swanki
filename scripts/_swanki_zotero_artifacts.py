"""
scripts/_swanki_zotero_artifacts.py
[[scripts._swanki_zotero_artifacts]]
https://github.com/Mjvolk3/Swanki/tree/main/scripts/_swanki_zotero_artifacts.py
Test file: tests/test_swanki_anki_sync.py

Thin re-export shim. The "newest artifact per content-prefix" logic moved
into the installed package at ``swanki/delivery/artifacts.py`` so the delivery
subsystem and the script CLIs share one implementation. This module keeps the
historical import path (and names) the scripts and tests already use.
"""

from swanki.delivery.artifacts import (
    APKG_PATTERN as APKG_PATTERN,
)
from swanki.delivery.artifacts import (
    ZIP_PATTERN as ZIP_PATTERN,
)
from swanki.delivery.artifacts import (
    _latest_artifact as _latest_artifact,
)
from swanki.delivery.artifacts import (
    latest_apkgs as latest_apkgs,
)
from swanki.delivery.artifacts import (
    latest_zip as latest_zip,
)
from swanki.delivery.artifacts import (
    latest_zips as latest_zips,
)
