"""
tests/test_audio_fish_port_resolution.py
[[tests.test_audio_fish_port_resolution]]
https://github.com/Mjvolk3/Swanki/tree/main/tests/test_audio_fish_port_resolution.py

Fish Speech server discovery under the SLURM serverless model: a single-element
SWANKI_FISH_PORTS collapses discovery to exactly one job-private port (no probing
of the legacy 8080-8083 fleet).
"""

import swanki.audio._common as common


class _Resp:
    def __init__(self, status_code: int) -> None:
        self.status_code = status_code


def _reset_discovery(monkeypatch, ports):
    monkeypatch.setattr(common, "_FISH_SPEECH_PORTS", ports)
    monkeypatch.setattr(common, "_servers_discovered", False)
    monkeypatch.setattr(common, "_healthy_servers", [])


def test_single_port_probes_only_that_port(monkeypatch):
    _reset_discovery(monkeypatch, [8123])
    probed: list[str] = []

    def fake_get(url, timeout=0.0):
        probed.append(url)
        return _Resp(200)

    monkeypatch.setattr(common.httpx, "get", fake_get)
    servers = common._discover_fish_speech_servers("http://127.0.0.1:8123")

    assert servers == ["http://127.0.0.1:8123"]
    assert probed == ["http://127.0.0.1:8123/v1/health"]


def test_single_port_unhealthy_falls_back_to_base_url(monkeypatch):
    _reset_discovery(monkeypatch, [8123])

    def fake_get(url, timeout=0.0):
        raise common.httpx.HTTPError("connection refused")

    monkeypatch.setattr(common.httpx, "get", fake_get)
    # Fallback is the base_url, which for the serverless job is the same single
    # port, so the picker still targets the job's own server once it is up.
    servers = common._discover_fish_speech_servers("http://127.0.0.1:8123")
    assert servers == ["http://127.0.0.1:8123"]


def test_picker_returns_the_single_server(monkeypatch):
    _reset_discovery(monkeypatch, [8123])
    monkeypatch.setattr(common.httpx, "get", lambda url, timeout=0.0: _Resp(200))
    assert common._pick_fish_speech_server("http://127.0.0.1:8123") == (
        "http://127.0.0.1:8123"
    )
