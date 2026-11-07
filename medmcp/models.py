"""Typed data models for the MedMCP knowledge base.

The IEC 62304 knowledge base is represented as a flat collection of
:class:`KnowledgeEntry` objects. Each entry corresponds to a clause, sub-clause,
or a defined concept from the standard.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

# Top-level processes in IEC 62304.
Category = Literal[
    "general",        # clauses 1-4: scope, references, terms, general requirements
    "development",    # clause 5: software development process
    "maintenance",    # clause 6: software maintenance process
    "risk",           # clause 7: software risk management process
    "configuration",  # clause 8: software configuration management process
    "problem",        # clause 9: software problem resolution process
    "concept",        # terms & definitions (clause 3) and cross-cutting concepts
]

# Software safety classifications defined in IEC 62304 clause 4.3.
SafetyClass = Literal["A", "B", "C"]


class KnowledgeEntry(BaseModel):
    """A single unit of knowledge (a clause, sub-clause or concept)."""

    id: str = Field(description="Stable identifier; usually the clause number, e.g. '5.1.3'.")
    clause: str = Field(description="Human-readable clause reference, e.g. '5.1.3'.")
    title: str = Field(description="Short title of the clause or concept.")
    content: str = Field(description="Explanatory content: what the clause requires.")
    category: Category = "general"
    keywords: list[str] = Field(default_factory=list, description="Search keywords.")
    related: list[str] = Field(default_factory=list, description="Related clause ids.")
    safety_class: SafetyClass | None = Field(
        default=None, description="Safety class this requirement applies to, if specific."
    )
    source: str = Field(default="builtin", description="Origin: 'builtin' or a document name.")

    def searchable_text(self) -> str:
        """All text that participates in semantic (TF-IDF) indexing."""
        parts = [
            self.clause,
            self.title,
            self.content,
            *self.keywords,
        ]
        return " ".join(parts)


class SearchResult(BaseModel):
    """A ranked search hit."""

    entry: KnowledgeEntry
    score: float = Field(description="Normalized relevance score (higher is better).")
    match_type: str = Field(description="How the hit matched: 'keyword', 'semantic', or 'hybrid'.")


class SafetyClassInfo(BaseModel):
    """Requirements summary for one software safety class."""

    safety_class: SafetyClass
    description: str
    risk_criterion: str
    applicable_clauses: list[str]


__all__ = [
    "Category",
    "SafetyClass",
    "KnowledgeEntry",
    "SearchResult",
    "SafetyClassInfo",
]
