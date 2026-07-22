"""
swanki/delivery/__main__.py
[[swanki.delivery.__main__]]
https://github.com/Mjvolk3/Swanki/tree/main/swanki/delivery/__main__.py
Test file: tests/test_delivery_orchestrator.py

CLI entry for the delivery subsystem, invoked by the queue drainer:

    python -m swanki.delivery deliver --citation-key K --content-key C \
        --output-dir D --audio-prefix P [--source local|zotero] \
        [--targets zotero,anki,abs] [--merge-tracks auto|lecture,...] [--dry-run]
    python -m swanki.delivery finalize-abs [--dry-run]

``deliver`` runs one job's Zotero -> Anki delivery and defers ABS;
``finalize-abs`` fires the single debounced ABS refresh after the queue drains.
Defaults (source, enabled targets) are read from the Hydra ``delivery`` config
group so the same knobs drive both the CLI and any in-pipeline use.
"""

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml  # type: ignore[import-untyped]
from dotenv import load_dotenv

from swanki.delivery.markers import TARGET_ORDER
from swanki.delivery.orchestrator import _repo_dir, deliver
from swanki.delivery.targets.abs import AbsTarget

_CONF_DIR = Path(__file__).resolve().parents[1] / "conf" / "delivery"


def _load_defaults(variant: str) -> dict[str, Any]:
    """Load source + target defaults from a ``conf/delivery/*.yaml`` variant."""
    path = _CONF_DIR / f"{variant}.yaml"
    raw = yaml.safe_load(path.read_text())
    return dict(raw["delivery"])


def _enabled_targets(cfg: dict[str, Any], override: str | None) -> list[str]:
    """Resolve the enabled-target list from config, honoring a CLI override."""
    if override is not None:
        return [t.strip() for t in override.split(",") if t.strip()]
    toggles = cfg.get("targets", {})
    return [t for t in TARGET_ORDER if toggles.get(t, True)]


def _parse_merge_tracks(raw: str | None) -> set[str] | str | None:
    """Parse the ``--merge-tracks`` value into the shape ``deliver`` expects.

    Args:
        raw: ``None`` (full replace), ``"auto"``, or a comma list of tracks.

    Returns:
        ``None``, the literal ``"auto"``, or a set of track names.
    """
    if raw is None:
        return None
    if raw.strip() == "auto":
        return "auto"
    return {t.strip() for t in raw.split(",") if t.strip()}


def _cmd_deliver(args: argparse.Namespace) -> int:
    cfg = _load_defaults(args.config)
    source_kind = args.source or cfg.get("source", "local")
    enabled = _enabled_targets(cfg, args.targets)
    result = deliver(
        citation_key=args.citation_key,
        content_key=args.content_key or args.citation_key,
        output_dir=Path(args.output_dir),
        audio_prefix=args.audio_prefix,
        source_kind=source_kind,
        enabled=enabled,
        defer_abs=not args.run_abs,
        dry_run=args.dry_run,
        merge_tracks=_parse_merge_tracks(args.merge_tracks),
    )
    print(
        f"delivered={result.delivered} ran={result.ran} "
        f"abs_deferred={result.abs_deferred}"
    )
    return 0 if result.delivered else 1


def _cmd_finalize_abs(args: argparse.Namespace) -> int:
    AbsTarget(_repo_dir()).refresh(dry_run=args.dry_run)
    return 0


def main(argv: list[str] | None = None) -> int:
    """Parse args and dispatch the delivery subcommand."""
    load_dotenv()
    parser = argparse.ArgumentParser(prog="python -m swanki.delivery")
    parser.add_argument(
        "--config",
        default="default",
        help="conf/delivery variant for defaults (default: %(default)s)",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("deliver", help="deliver one job (Zotero -> Anki; defer ABS)")
    d.add_argument("--citation-key", required=True)
    d.add_argument("--content-key", default="")
    d.add_argument("--output-dir", required=True)
    d.add_argument("--audio-prefix", required=True)
    d.add_argument("--source", choices=["local", "zotero"], default=None)
    d.add_argument("--targets", default=None, help="comma list, e.g. zotero,anki")
    d.add_argument(
        "--merge-tracks",
        default=None,
        help="Zotero merge policy for a partial regen: 'auto' (merge only the "
        "tracks present in the output dir) or a comma list "
        "(lecture,summary,reading,cards). Omit for full-replace.",
    )
    d.add_argument(
        "--run-abs",
        action="store_true",
        help="run ABS refresh inline instead of deferring it",
    )
    d.add_argument("--dry-run", action="store_true")
    d.set_defaults(func=_cmd_deliver)

    f = sub.add_parser("finalize-abs", help="run the debounced ABS refresh once")
    f.add_argument("--dry-run", action="store_true")
    f.set_defaults(func=_cmd_finalize_abs)

    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    sys.exit(main())
