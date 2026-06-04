"""
swanki/delivery/__init__.py
[[swanki.delivery]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/delivery/__init__.py

Configurable delivery subsystem: a SyncSource axis (where canonical artifacts
come from -- ``local`` on-disk output or ``zotero``) crossed with a SyncTarget
axis (per server -- ``anki``, ``abs``, and the ``zotero`` backup sink). The
``deliver`` orchestrator runs the enabled targets in the order
Zotero -> Anki -> ABS and records per-target ``.delivery.json`` markers so the
queue's DONE means "generated AND delivered", crash-resumable.
"""

from swanki.delivery.markers import TARGET_ORDER as TARGET_ORDER
from swanki.delivery.markers import DeliveryMarkers as DeliveryMarkers
from swanki.delivery.orchestrator import DeliveryResult as DeliveryResult
from swanki.delivery.orchestrator import deliver as deliver
from swanki.delivery.source import ArtifactSet as ArtifactSet
from swanki.delivery.source import LocalSource as LocalSource
from swanki.delivery.source import SyncSource as SyncSource
from swanki.delivery.source import ZoteroSource as ZoteroSource
