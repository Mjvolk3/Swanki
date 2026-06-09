"""
tests/test_abs_projections.py
[[tests.test_abs_projections]]
https://github.com/Mjvolk3/Swanki/tree/main/tests/test_abs_projections.py
Test file: tests/test_abs_projections.py

Tests for swanki/abs/projections.py (citation-key fallback chain, routing
helpers, projections.yml loading) and the library index/lookup helpers in
swanki/abs/libraries.py. Fixture YAML; mocked transport; no infra access.
"""

import httpx

from swanki.abs.client import ABSClient
from swanki.abs.libraries import build_library_index, library_items_by_title
from swanki.abs.projections import (
    citation_key,
    classify,
    group_key,
    kind_for_key,
    load_projections,
    resolve_library,
)

# -- citation-key fallback chain (load-bearing; three cases) -------------------


def test_citation_key_explicit_field():
    item = {"key": "ZK1", "data": {"citationKey": "hamming2020"}}
    assert citation_key(item) == "hamming2020"


def test_citation_key_extra_regex():
    item = {
        "key": "ZK1",
        "data": {"citationKey": "", "extra": "Citation Key: bechtel1986\nfoo"},
    }
    assert citation_key(item) == "bechtel1986"


def test_citation_key_falls_back_to_item_key():
    item = {"key": "ZK1", "data": {"extra": "no key here"}}
    assert citation_key(item) == "ZK1"


# -- routing -------------------------------------------------------------------


def test_classify_and_group_key():
    book = {"data": {"itemType": "bookSection"}}
    paper = {"data": {"itemType": "journalArticle"}}
    assert classify(book) == "Book"
    assert classify(paper) == "Paper"
    assert (
        group_key("hammingArtDoingScience2020_CH02_foundations", "Book")
        == "hammingArtDoingScience2020"
    )
    assert group_key("smith2024", "Paper") == "smith2024"


def test_kind_for_key_infers_from_chapter_suffix():
    assert kind_for_key("hammingArtDoingScience2020_CH02_foundations") == "Book"
    assert kind_for_key("smith2024") == "Paper"


def test_resolve_library_literal_and_env(monkeypatch):
    assert resolve_library({"library_id": 42}) == ("42", "user")
    monkeypatch.setenv("MY_LIB_ID", "777")
    assert resolve_library(
        {"library_id_env": "MY_LIB_ID", "library_type": "group"}
    ) == ("777", "group")


def test_load_projections_fixture(tmp_path):
    yml = tmp_path / "projections.yml"
    yml.write_text(
        "projections:\n"
        "  mv-ll:\n"
        "    audiotypes: [summary, lecture]\n"
        "    push_audio: true\n"
        "    zotero: {library_id: 1, tag: fox}\n"
        "  quiet:\n"
        "    audiotypes: [lecture]\n"
        "    push_audio: false\n"
        "    zotero: {library_id: 2}\n"
    )
    projections = load_projections(yml)
    assert set(projections) == {"mv-ll", "quiet"}
    assert projections["mv-ll"]["audiotypes"] == ["summary", "lecture"]
    assert projections["quiet"]["push_audio"] is False


# -- library index + title lookup ----------------------------------------------

LIBS_JSON = {
    "libraries": [
        {
            "id": "L1",
            "name": "Book — Lecture",
            "folders": [{"fullPath": "/audiobooks/mv-ll/Swanki-Book-Lecture"}],
        },
        {
            "id": "L2",
            "name": "Paper — Summary",
            "folders": [{"fullPath": "/audiobooks/mv-ll/Swanki-Paper-Summary"}],
        },
        {
            "id": "L3",
            "name": "Podcasts",
            "folders": [{"fullPath": "/podcasts"}],
        },
    ]
}


def _client(handler) -> ABSClient:
    return ABSClient(
        base_url="https://abs.test",
        token="tok",
        transport=httpx.MockTransport(handler),
    )


def test_build_library_index_lowercases_audiotype():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=LIBS_JSON)

    index = build_library_index(_client(handler))
    # Non-swanki folder (L3) skipped; audiotype normalized to lowercase.
    assert index == {
        ("mv-ll", "Book", "lecture"): "L1",
        ("mv-ll", "Paper", "summary"): "L2",
    }


def test_library_items_by_title_falls_back_to_path():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={
                "results": [
                    {
                        "id": "I1",
                        "media": {"metadata": {"title": "hamming2020"}},
                    },
                    {
                        "id": "I2",
                        "media": {"metadata": {}},
                        "path": "/audiobooks/x/Swanki-Book-Lecture/bechtel1986",
                    },
                ]
            },
        )

    items = library_items_by_title(_client(handler), "L1")
    assert items == {"hamming2020": "I1", "bechtel1986": "I2"}
