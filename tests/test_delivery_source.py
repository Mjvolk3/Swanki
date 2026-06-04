"""
tests/test_delivery_source.py
[[tests.test_delivery_source]]
https://github.com/Mjvolk3/Swanki/tree/main/tests/test_delivery_source.py

Unit tests for the SyncSource layer (``swanki/delivery/source.py``).
``LocalSource`` globs an on-disk output dir; ``ArtifactSet`` is the resolved
result. No live network (ZoteroSource integration is exercised via the
orchestrator tests with mocks).
"""

from pathlib import Path

from swanki.delivery.source import ArtifactSet, LocalSource


class TestArtifactSet:
    def test_is_empty(self) -> None:
        assert ArtifactSet(key="k", content_key="k").is_empty
        assert not ArtifactSet(
            key="k", content_key="k", apkgs=(Path("a.apkg"),)
        ).is_empty


class TestLocalSource:
    def test_resolves_apkg_and_audio(self, tmp_path: Path) -> None:
        (tmp_path / "bishop2024.apkg").write_bytes(b"x")
        (tmp_path / "bishop2024-fish-summary-audio.mp3").write_bytes(b"x")
        (tmp_path / "bishop2024-fish-lecture-audio.mp3").write_bytes(b"x")
        (tmp_path / "bishop2024-fish-reading-audio.mp3").write_bytes(b"x")
        (tmp_path / "notes.md").write_text("ignore")  # non-artifact

        result = LocalSource(tmp_path).resolve("bishop2024", "bishop2024")
        assert [p.name for p in result.apkgs] == ["bishop2024.apkg"]
        assert len(result.audio) == 3
        assert all(p.suffix == ".mp3" for p in result.audio)

    def test_picks_up_problem_set_apkg(self, tmp_path: Path) -> None:
        (tmp_path / "alcamo.apkg").write_bytes(b"x")
        (tmp_path / "alcamo-problem-set.apkg").write_bytes(b"x")
        result = LocalSource(tmp_path).resolve("alcamo", "alcamo")
        assert sorted(p.name for p in result.apkgs) == [
            "alcamo-problem-set.apkg",
            "alcamo.apkg",
        ]

    def test_missing_dir_is_empty(self, tmp_path: Path) -> None:
        result = LocalSource(tmp_path / "nope").resolve("k", "k")
        assert result.is_empty

    def test_no_artifacts_is_empty(self, tmp_path: Path) -> None:
        (tmp_path / "stuff.txt").write_text("x")
        assert LocalSource(tmp_path).resolve("k", "k").is_empty
