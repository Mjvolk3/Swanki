---
id: 96iu9venu93206ioet74520
title: Abs_bookmarks
desc: ''
updated: 1779147290337
created: 1779147290337
---

## 2026.05.18 - ABS bookmark fetcher (replaces macOS BookPlayer sqlite)

The legacy `/fetch-bookmarks` skill reads a macOS BookPlayer SQLite path
(`/Users/...Library/...`) that does not exist on gilahyper. This script
fetches the current user's bookmarks from the Audiobookshelf REST API
instead: `GET {ABS_URL}/api/me` with a bearer token from
`ABS_API_TOKEN_FILE` (defaults mirror `scripts/abs_refresh.sh`:
`https://abs.michaelvolk.dev`, `~/Documents/projects/infra/abs/.api-token`).

Mirrors `scripts/zotero_annotations.py`: frontmatter docstring, explicit
`load_dotenv(dotenv_path=...)` (cwd not guaranteed), pydantic `AbsBookmark`,
importable `get_bookmarks(*, citation_key=None)` + thin argparse CLI. The
`/api/me` JSON->model mapping is isolated in `_to_bookmark` so a schema
drift is a one-line, fixture-tested fix
(`tests/test_abs_bookmarks.py`, fully mocked -- no network/token).
Consumed by the `/audio-fix-from-annotations` skill; a bookmark `time` is
the playhead WHEN SAVED (lags the issue by minutes) so it only narrows the
chapter/audio_type -- the chunk is found by content-match + the
`chunk_timeline.json` sidecar
([[plan.exact-chunk-time-mapping-audio-fix-from-annotations.2026.05.18]]).
