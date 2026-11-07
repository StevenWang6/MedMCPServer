"""MedMCP server: tools and resources exposing the IEC 62304 knowledge base.

The server is built with the official MCP SDK's :class:`~mcp.server.fastmcp.FastMCP`
high-level API and exposes:

Tools
    * ``search_62304`` — hybrid keyword + semantic search.
    * ``get_clause`` — exact clause / sub-clause lookup.
    * ``list_clauses`` — enumerate clauses, optionally filtered by category.
    * ``safety_class_info`` — requirements summary for Class A/B/C.
    * ``index_documents`` — (re)index user documents from the documents directory.
    * ``list_documents`` — list the indexed documents.

Resources
    * ``medmcp://knowledge`` — the full knowledge base as JSON.
    * ``medmcp://clause/{clause}`` — a single clause as JSON.
"""

from __future__ import annotations

import os
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from medmcp.documents import DEFAULT_DOCUMENTS_DIR, load_documents
from medmcp.knowledge import SAFETY_CLASSES, get_all_entries, get_entry
from medmcp.models import KnowledgeEntry, SafetyClass
from medmcp.search import SearchEngine, build_search_engine

SERVER_NAME = "medmcp"

INSTRUCTIONS = (
    "MedMCP provides query access to an IEC 62304 medical device software life-cycle "
    "knowledge base. Use the search tools to look up clauses, requirements, safety "
    "classification guidance, and cross-cutting concepts such as SOUP and traceability."
)


def _entry_to_dict(entry: KnowledgeEntry) -> dict:
    return {
        "id": entry.id,
        "clause": entry.clause,
        "title": entry.title,
        "category": entry.category,
        "content": entry.content,
        "keywords": entry.keywords,
        "related": entry.related,
        "safety_class": entry.safety_class,
        "source": entry.source,
    }


def _format_result(result) -> dict:
    entry = result.entry
    d = _entry_to_dict(entry)
    d["score"] = result.score
    d["match_type"] = result.match_type
    return d


class MedMCPServer:
    """Holds the knowledge state and registers MCP tools/resources."""

    def __init__(
        self,
        *,
        documents_dir: str | Path | None = None,
        use_embeddings: bool = False,
        index_on_startup: bool | None = None,
        host: str = "127.0.0.1",
        port: int = 8000,
    ) -> None:
        self.documents_dir = Path(documents_dir) if documents_dir else DEFAULT_DOCUMENTS_DIR

        self.builtin_entries: list[KnowledgeEntry] = get_all_entries()
        self.document_entries: list[KnowledgeEntry] = []

        self.engine: SearchEngine = build_search_engine(
            self.builtin_entries, use_embeddings=use_embeddings
        )

        if index_on_startup is None:
            index_on_startup = os.environ.get("MEDMCP_INDEX_ON_STARTUP", "0") == "1"
        if index_on_startup:
            self.index_documents()

        self.mcp = FastMCP(
            SERVER_NAME,
            instructions=INSTRUCTIONS,
            host=host,
            port=port,
        )
        self._register()

    # ------------------------------------------------------------ public API
    def all_entries(self) -> list[KnowledgeEntry]:
        return [*self.builtin_entries, *self.document_entries]

    def rebuild_engine(self) -> None:
        """Rebuild the search index from the current entry set."""
        self.engine = build_search_engine(self.all_entries())

    def index_documents(self, directory: str | Path | None = None) -> dict:
        """(Re)index documents and refresh the search engine."""
        target = Path(directory) if directory else self.documents_dir
        entries, errors = load_documents(target)
        self.document_entries = entries
        self.rebuild_engine()
        return {
            "indexed_entries": len(entries),
            "documents": sorted({e.source for e in entries}),
            "errors": errors,
        }

    def list_documents(self) -> dict:
        sources = sorted({e.source for e in self.document_entries})
        return {
            "documents": sources,
            "count": len(sources),
        }

    # ---------------------------------------------------------------- tools
    def search_62304(
        self,
        query: str,
        mode: str = "hybrid",
        top_k: int = 5,
        include_related: bool = False,
    ) -> dict:
        """Search the IEC 62304 knowledge base.

        ``mode`` may be ``keyword`` (exact clause numbers and keywords), ``semantic``
        (TF-IDF cosine similarity) or ``hybrid`` (weighted combination, default).
        """
        top_k = max(1, min(int(top_k), 20))
        results = self.engine.search(query, top_k=top_k, mode=mode)

        hits = [_format_result(r) for r in results]
        if include_related:
            for hit in hits:
                hit["related_entries"] = [
                    _entry_to_dict(e)
                    for eid in hit.get("related", [])
                    if (e := get_entry(eid))
                ]
        return {
            "query": query,
            "mode": mode,
            "total": len(hits),
            "results": hits,
        }

    def get_clause(self, clause: str, include_related: bool = False) -> dict:
        """Return a specific clause or concept by its reference (e.g. '5.1.3', '4.3', 'SOUP')."""
        entry = get_entry(clause.strip())
        if entry is None:
            # Fall back to a search to offer suggestions.
            suggestions = [
                _format_result(r)
                for r in self.engine.search(clause, top_k=3, mode="hybrid")
            ]
            return {
                "found": False,
                "clause": clause,
                "message": f"No exact match for '{clause}'.",
                "suggestions": suggestions,
            }

        data = _entry_to_dict(entry)
        if include_related:
            data["related_entries"] = [
                _entry_to_dict(e) for eid in entry.related if (e := get_entry(eid))
            ]
        return {"found": True, "entry": data}

    def list_clauses(
        self,
        category: str | None = None,
        query: str | None = None,
    ) -> dict:
        """List clauses/concepts in the knowledge base.

        Optionally filter by ``category`` (general, development, maintenance, risk,
        configuration, problem, concept) and/or a text ``query``.
        """
        entries = self.all_entries()
        if category:
            entries = [e for e in entries if e.category == category]
        if query:
            q = query.lower()
            entries = [
                e
                for e in entries
                if q in e.title.lower() or q in e.content.lower() or q in e.clause.lower()
            ]

        listing = [
            {
                "id": e.id,
                "clause": e.clause,
                "title": e.title,
                "category": e.category,
                "safety_class": e.safety_class,
                "source": e.source,
            }
            for e in entries
        ]
        return {"count": len(listing), "clauses": listing}

    def safety_class_info(self, safety_class: str) -> dict:
        """Return the definition and applicable requirements for Class A, B or C software."""
        key = safety_class.strip().upper()
        if key not in SAFETY_CLASSES:
            return {
                "found": False,
                "safety_class": safety_class,
                "message": "Safety class must be one of 'A', 'B' or 'C'.",
            }

        info = dict(SAFETY_CLASSES[key])
        info["clause_entries"] = [
            _entry_to_dict(e)
            for cid in info.get("applicable_clauses", [])
            if (e := get_entry(cid))
        ]
        info["found"] = True
        return info

    # ------------------------------------------------------------ resources
    def resource_knowledge(self) -> str:
        import json

        return json.dumps(
            [_entry_to_dict(e) for e in self.all_entries()],
            ensure_ascii=False,
            indent=2,
        )

    def resource_clause(self, clause: str) -> str:
        import json

        entry = get_entry(clause)
        if entry is None:
            return json.dumps({"found": False, "clause": clause})
        return json.dumps(_entry_to_dict(entry), ensure_ascii=False, indent=2)

    # --------------------------------------------------------- registration
    def _register(self) -> None:
        mcp = self.mcp

        mcp.tool()(self.search_62304)
        mcp.tool()(self.get_clause)
        mcp.tool()(self.list_clauses)
        mcp.tool()(self.safety_class_info)
        mcp.tool()(self.index_documents)
        mcp.tool()(self.list_documents)

        mcp.resource("medmcp://knowledge")(self.resource_knowledge)
        mcp.resource("medmcp://clause/{clause}")(self.resource_clause)


def create_server(
    *,
    documents_dir: str | Path | None = None,
    use_embeddings: bool = False,
    index_on_startup: bool | None = None,
    host: str = "127.0.0.1",
    port: int = 8000,
) -> MedMCPServer:
    """Create a configured :class:`MedMCPServer` instance."""
    return MedMCPServer(
        documents_dir=documents_dir,
        use_embeddings=use_embeddings,
        index_on_startup=index_on_startup,
        host=host,
        port=port,
    )


def build_server(
    *,
    documents_dir: str | Path | None = None,
    use_embeddings: bool = False,
    index_on_startup: bool | None = None,
    host: str = "127.0.0.1",
    port: int = 8000,
) -> FastMCP:
    """Create and return the underlying :class:`FastMCP` instance."""
    return create_server(
        documents_dir=documents_dir,
        use_embeddings=use_embeddings,
        index_on_startup=index_on_startup,
        host=host,
        port=port,
    ).mcp


__all__ = [
    "SERVER_NAME",
    "INSTRUCTIONS",
    "MedMCPServer",
    "create_server",
    "build_server",
]
