---
id: hk7w8m2x4znq3p9r5tvy6u
title: Headless Anki Sync on Gilahyper
desc: Headless Anki desktop on gilahyper acting as a push-only AnkiWeb client for generated .apkg decks.
updated: 1779931980000
created: 1779931980000
---

Headless Anki desktop running on gilahyper as a second AnkiWeb client. The Swanki pipeline pushes generated `.apkg` files into it via AnkiConnect; it syncs them up to AnkiWeb; the Mac Anki pulls them down on next sync.

## Architecture

```
Swanki pipeline -- importPackage / sync (AnkiConnect HTTP :8765)
        |
        v
Headless Anki desktop on gilahyper (Xvfb :99, no GUI)
        |
        v  normal Anki sync
AnkiWeb (existing account, shared with Mac)
        |
        v  Mac clicks Sync
Mac Anki desktop (untouched study client)
```

Two Anki "devices" on one AnkiWeb account; AnkiWeb is the merge point. Notes dedupe by GUID on import.

## Why not direct upload to AnkiWeb

AnkiWeb has no public API for uploading `.apkg`. The self-hosted sync server also rejects file copies -- it's a sync endpoint only. The only programmatic path is a *running Anki client* + AnkiConnect, which is what this setup provides.

## Files

| Path | Purpose |
|---|---|
| `~/bin/anki-headless.sh` | Service wrapper -- starts Xvfb on :99, then `exec`s `flatpak run net.ankiweb.Anki`. Cleans stale `/tmp/.X99-lock` + `prefs21.db-journal` on startup. |
| `~/bin/anki-vnc-attach.sh` | On-demand VNC: x11vnc against :99 + websockify on :6080 for browser viewing. Run only when debugging. |
| `~/bin/anki-vnc-detach.sh` | Stops x11vnc + websockify; Anki keeps running. |
| `~/.config/systemd/user/anki-headless.service` | systemd `--user` unit. `Type=simple`, `Restart=on-failure`. |
| `~/bin/anki-headless-login.sh` | One-shot bootstrap (Xvfb + Anki + x11vnc + websockify) used for the initial AnkiWeb login. Superseded by the systemd service; kept for reference. |

Linger is enabled (`sudo loginctl enable-linger michaelvolk`) so the unit survives SSH disconnect and reboot.

## Operational commands

```bash
# service control
systemctl --user start|stop|restart|status anki-headless
journalctl --user -u anki-headless -f

# peek at the running headless Anki (browser, no client install)
~/bin/anki-vnc-attach.sh
# forward port 6080 in VS Code, then open in browser:
#   http://localhost:6080/vnc.html?host=localhost&port=6080&path=websockify
~/bin/anki-vnc-detach.sh

# talk to AnkiConnect
curl -s -X POST http://127.0.0.1:8765 \
  -H 'Content-Type: application/json' \
  -d '{"action":"version","version":6}'
```

AnkiConnect listens on `127.0.0.1:8765` only -- not reachable off-host.

## Push workflow (.apkg -> AnkiWeb -> Mac)

Three AnkiConnect calls per push:

1. `deleteDecks` with `cardsToo: true` (optional, dev-only "overwrite" mode) -- wipes the named deck on gilahyper before re-import. Without it, `importPackage` merges by note GUID: same GUID updates, new GUID adds.
2. `importPackage` with `{"path": "/abs/path/to/deck.apkg"}` -- loads notes/cards/media into the headless collection.
3. `sync` -- pushes to AnkiWeb. Mac picks it up on its next Sync.

Card GUID stability matters: if the Swanki generator assigns stable GUIDs per source content, normal merge-by-GUID is the right behavior and the `deleteDecks` step is only needed when the deck schema changes.

## Setup history (2026-05-25 -> 2026-05-26)

1. `sudo dnf install xorg-x11-server-Xvfb x11vnc novnc python3-websockify` (Rocky 9.5).
2. `flatpak --user install flathub net.ankiweb.Anki` (currently 25.09.04).
3. Bootstrap `~/bin/anki-headless-login.sh` to launch Xvfb + Anki + noVNC; forwarded port 6080 in VS Code and logged into AnkiWeb via the browser. Chose **Download from AnkiWeb** on the first-sync direction prompt (Mac collection was the source of truth).
4. Installed AnkiConnect addon via Anki's GUI (Tools -> Add-ons -> Get Add-ons, code `2055492159`).
5. Cut over to systemd: wrote `~/bin/anki-headless.sh` + `anki-headless.service`, enabled linger, `systemctl --user enable --now anki-headless`.
6. Verified `curl POST {action:version}` returns `{"result": 6, "error": null}`.

## Troubleshooting

- **"Already running; reusing existing instance" + `sqlite3.OperationalError: database is locked`**: a previous crashed Anki left a journal file. Fix: `flatpak kill net.ankiweb.Anki && rm -f ~/.var/app/net.ankiweb.Anki/data/Anki2/prefs21.db-journal`. The service wrapper does this on every start.
- **Service won't start, Xvfb error about `/tmp/.X99-lock`**: stale lock from a crash. The wrapper removes both `/tmp/.X99-lock` and `/tmp/.X11-unix/X99` on startup.
- **Harmless DBus warning** in journal (`Failed to connect to socket /run/dbus/system_bus_socket`): expected -- flatpak runs without the system bus. No functional impact.
- **AnkiConnect returns nothing**: confirm Anki process is actually up (`systemctl --user status anki-headless`); the addon only binds the port once Anki's main loop is running.

## Related

- [[swanki.processing.apkg_exporter]] -- the generator that produces the `.apkg` files this setup consumes.
- Future: `anki=ankiconnect` mode in the Swanki pipeline that POSTs `importPackage` + `sync` instead of writing only to disk.
