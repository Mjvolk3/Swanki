"""
swanki/delivery/targets/__init__.py
[[swanki.delivery.targets]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/delivery/targets/__init__.py

SyncTarget implementations: each consumes an ``ArtifactSet`` from a source and
pushes it to one self-hosted server (Anki, ABS) or the Zotero backup sink.
"""

from swanki.delivery.targets.abs import AbsTarget as AbsTarget
from swanki.delivery.targets.anki import AnkiTarget as AnkiTarget
from swanki.delivery.targets.zotero import ZoteroBackupTarget as ZoteroBackupTarget
