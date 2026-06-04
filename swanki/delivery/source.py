"""
swanki/delivery/source.py
[[swanki.delivery.source]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/delivery/source.py
Test file: tests/test_delivery_source.py

The SyncSource axis of the delivery subsystem: where canonical artifacts come
from. ``LocalSource`` reads the on-disk pipeline output directory (the default,
no network round-trip); ``ZoteroSource`` downloads the newest attachments from
Zotero (for users without on-disk data). Both yield an ``ArtifactSet`` the
targets consume.
"""

import logging
import os
from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol

from pyzotero import zotero

from swanki.delivery.artifacts import latest_apkgs, latest_zips
from swanki.sync.zotero_client import make_zotero_client, with_zotero_retry

logger = logging.getLogger(__name__)

# Audio mp3 stems the pipeline emits, keyed off the audio prefix.
_AUDIO_SUFFIXES = ("-summary-audio.mp3", "-reading-audio.mp3", "-lecture-audio.mp3")


@dataclass(frozen=True)
class ArtifactSet:
    """Resolved local artifacts for one citation/content key.

    Paths are always local files on disk (``ZoteroSource`` downloads to a
    staging dir before returning). ``apkgs`` feed the Anki target; ``audio``
    feeds the ABS target.
    """

    key: str
    content_key: str
    apkgs: tuple[Path, ...] = field(default_factory=tuple)
    audio: tuple[Path, ...] = field(default_factory=tuple)

    @property
    def is_empty(self) -> bool:
        """True when neither apkgs nor audio resolved."""
        return not self.apkgs and not self.audio


class SyncSource(Protocol):
    """Ground-truth resolver: yields the canonical artifacts for a key."""

    name: str

    def resolve(self, key: str, content_key: str) -> ArtifactSet:
        """Resolve local artifact paths for ``key`` / ``content_key``."""
        ...


class LocalSource:
    """Resolve artifacts straight from the pipeline's on-disk output dir.

    The default source: the apkg and audio mp3s already sit in ``output_dir``
    the moment the pipeline finishes, so delivery needs no network round-trip
    and never blocks on a flaky Zotero API.
    """

    name = "local"

    def __init__(self, output_dir: Path) -> None:
        """Store the pipeline output dir this source globs."""
        self.output_dir = output_dir

    def resolve(self, key: str, content_key: str) -> ArtifactSet:
        """Glob ``output_dir`` for the run's apkg(s) and audio mp3(s).

        A pipeline run writes one apkg (plus an optional ``-problem-set`` apkg)
        and the audio mp3s for this content key; there is no historical
        accumulation in ``output_dir``, so a direct glob is exact.

        Args:
            key: Citation key (Zotero lookup; unused locally but kept for
                interface symmetry).
            content_key: Content key naming the files; defaults to ``key``.

        Returns:
            An ``ArtifactSet`` of local paths. Empty when nothing matches.
        """
        if not self.output_dir.is_dir():
            logger.warning("LocalSource: output dir absent: %s", self.output_dir)
            return ArtifactSet(key=key, content_key=content_key)
        apkgs = tuple(sorted(self.output_dir.glob("*.apkg")))
        audio = tuple(
            p
            for suffix in _AUDIO_SUFFIXES
            for p in sorted(self.output_dir.glob(f"*{suffix}"))
        )
        return ArtifactSet(
            key=key, content_key=content_key, apkgs=apkgs, audio=audio
        )


class ZoteroSource:
    """Resolve artifacts by downloading the newest Zotero attachments.

    For users without on-disk pipeline output. Reads use the hardened client
    and ``with_zotero_retry`` so a transient 5xx/timeout does not abort. The
    zip's audio is left embedded -- the ABS target already extracts zips, so
    ``ZoteroSource`` returns the downloaded ``.zip`` and ``.apkg`` paths.
    """

    name = "zotero"

    def __init__(self, stage_dir: Path) -> None:
        """Store the staging dir downloads land in before delivery."""
        self.stage_dir = stage_dir

    def _client(self) -> zotero.Zotero:
        api_key = os.environ["ZOTERO_API_KEY"]
        library_id = os.environ["ZOTERO_LIBRARY_ID"]
        library_type = os.environ.get("ZOTERO_LIBRARY_TYPE", "user")
        return make_zotero_client(library_id, library_type, api_key)

    def _download(
        self,
        zot: zotero.Zotero,
        attachments: Iterable[dict[str, Any]],
        dest: Path,
    ) -> tuple[Path, ...]:
        dest.mkdir(parents=True, exist_ok=True)
        out: list[Path] = []
        for att in attachments:
            att_key = att["key"]
            # with_zotero_retry calls synchronously within this iteration, so
            # the closure over att_key has no late-binding hazard.
            content: bytes = with_zotero_retry(lambda: zot.file(att_key))
            target = dest / att["data"]["filename"]
            target.write_bytes(content)
            out.append(target)
        return tuple(out)

    def resolve(self, key: str, content_key: str) -> ArtifactSet:
        """Find the Zotero item for ``key`` and download its newest artifacts.

        Args:
            key: Citation key used for Zotero item lookup.
            content_key: Content key (used only for the staging subdir name).

        Returns:
            An ``ArtifactSet`` whose ``apkgs`` are downloaded ``.apkg`` files
            and whose ``audio`` are downloaded ``.zip`` files (the ABS target
            extracts the zip).
        """
        from swanki.sync.zotero import _find_zotero_item

        zot = self._client()
        item_key = with_zotero_retry(lambda: _find_zotero_item(zot, key))
        assert item_key, f"No Zotero item for citation key: {key}"
        dest = self.stage_dir / (content_key or key)
        apkgs = self._download(
            zot, with_zotero_retry(lambda: latest_apkgs(zot, item_key)), dest
        )
        zips = self._download(
            zot, with_zotero_retry(lambda: latest_zips(zot, item_key)), dest
        )
        return ArtifactSet(
            key=key, content_key=content_key, apkgs=apkgs, audio=zips
        )
