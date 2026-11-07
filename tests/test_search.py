"""Unit tests for the MedMCP knowledge base and search engine."""

from __future__ import annotations

import json
import re

import pytest

from medmcp.documents import load_documents
from medmcp.knowledge import BUILTIN_ENTRIES, get_all_entries, get_entry
from medmcp.search import SearchEngine
from medmcp.server import create_server


@pytest.fixture(scope="module")
def engine() -> SearchEngine:
    return SearchEngine(get_all_entries())


def test_knowledge_base_has_core_clauses() -> None:
    clauses = {e.clause for e in BUILTIN_ENTRIES}
    for required in ["1", "4", "4.3", "5", "5.1", "5.2", "5.3", "5.4", "5.5",
                     "5.6", "5.7", "5.8", "6", "7", "8", "9"]:
        assert required in clauses, f"missing clause {required}"


def test_all_entries_have_ids_and_content() -> None:
    for e in BUILTIN_ENTRIES:
        assert e.id
        assert e.title
        assert e.content.strip()


def test_get_entry_exact() -> None:
    e = get_entry("5.1.3")
    assert e is not None
    assert e.title == "Plan reference to system design and development"


def test_get_entry_missing_returns_none() -> None:
    assert get_entry("99.99") is None


def test_search_keyword_finds_exact_clause(engine: SearchEngine) -> None:
    results = engine.search("5.7.2", top_k=1, mode="keyword")
    assert results, "expected at least one result"
    assert results[0].entry.clause == "5.7.2"


def test_search_semantic_soup(engine: SearchEngine) -> None:
    results = engine.search("software of unknown provenance", top_k=1, mode="semantic")
    assert results
    assert results[0].entry.id == "soup"


def test_search_hybrid_safety_classification(engine: SearchEngine) -> None:
    results = engine.search("software safety classification", top_k=1, mode="hybrid")
    assert results
    assert results[0].entry.clause == "4.3"


def test_search_top_k_respects_limit(engine: SearchEngine) -> None:
    results = engine.search("risk management", top_k=3, mode="hybrid")
    assert len(results) <= 3


def test_document_ingestion_json_and_markdown(tmp_path) -> None:
    (tmp_path / "custom.json").write_text(
        json.dumps(
            [
                {
                    "id": "ext-1",
                    "clause": "annex-a",
                    "title": "Custom requirement",
                    "content": "Custom content about verification.",
                    "keywords": ["verification"],
                    "category": "development",
                }
            ]
        ),
        encoding="utf-8-sig",
    )
    (tmp_path / "custom.md").write_text(
        "# Section One\n\nContent one.\n\n## Section Two\n\nContent two.\n",
        encoding="utf-8-sig",
    )

    entries, errors = load_documents(tmp_path)
    assert errors == []
    sources = {e.source for e in entries}
    assert "document:custom.json" in sources
    assert "document:custom.md" in sources
    assert len(entries) == 3  # 1 JSON + 2 markdown sections


def test_document_ingestion_handles_bom(tmp_path) -> None:
    # Write with a UTF-8 BOM to simulate Windows editors.
    raw = b"\xef\xbb\xbf# BOM Heading\n\nBody text.\n"
    (tmp_path / "bom.md").write_bytes(raw)
    entries, errors = load_documents(tmp_path)
    assert errors == []
    assert len(entries) == 1
    assert entries[0].title == "BOM Heading"


def test_server_search_tool() -> None:
    s = create_server()
    r = s.search_62304("integration testing", top_k=2)
    assert r["total"] >= 1
    assert any("integration" in hit["title"].lower() for hit in r["results"])


def test_server_get_clause_with_suggestion() -> None:
    s = create_server()
    r = s.get_clause("does-not-exist")
    assert r["found"] is False
    assert "suggestions" in r


def test_server_safety_class_info() -> None:
    s = create_server()
    r = s.safety_class_info("c")
    assert r["found"] is True
    assert "death" in r["description"].lower()
    assert "4.3" in r["applicable_clauses"]


def test_safety_class_info_invalid() -> None:
    s = create_server()
    r = s.safety_class_info("D")
    assert r["found"] is False


def test_list_clauses_filter() -> None:
    s = create_server()
    r = s.list_clauses(category="risk")
    assert r["count"] > 0
    assert all(c["category"] == "risk" for c in r["clauses"])
