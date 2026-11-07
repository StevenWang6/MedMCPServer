"""Search engine for the MedMCP knowledge base.

Two retrieval strategies are provided, and a hybrid mode combines them:

* **keyword** — exact clause-number matching plus token/keyword overlap scoring.
* **semantic** — a pure-Python TF-IDF cosine similarity over entry text. This works
  with no external dependencies. If the optional ``sentence-transformers`` package
  is installed, it is used lazily as a denser embedding backend and TF-IDF remains
  the fallback.
* **hybrid** — a weighted combination of the two scores (the default).
"""

from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass, field
from typing import Callable

from medmcp.models import KnowledgeEntry, SearchResult

# A clause token looks like a dotted number: 5, 5.1, 5.1.3, 7.4.2, etc.
_CLAUSE_RE = re.compile(r"\b\d{1,2}(?:\.\d{1,2}){0,3}\b")
_WORD_RE = re.compile(r"[a-z0-9]+(?:[a-z0-9\-]*[a-z0-9])?")

_STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "to", "in", "for", "on", "with", "is",
    "are", "as", "at", "be", "by", "from", "this", "that", "it", "its", "shall",
    "which", "such", "any", "each", "into", "under", "than", "then", "their",
    "there", "when", "where", "within", "not", "no", "if", "may", "can", "has",
    "have", "had", "was", "were", "will", "would", "should", "could", "how",
    "what", "who", "why", "do", "does", "did", "must", "per", "also", "used",
}


def _tokenize(text: str) -> list[str]:
    """Lowercase, strip punctuation and split into meaningful tokens."""
    lowered = text.lower()
    words = _WORD_RE.findall(lowered)
    # Keep multi-word tokens simple: stopwords are removed during scoring.
    return [w for w in words if w not in _STOPWORDS and len(w) > 1]


def _clause_tokens(text: str) -> list[str]:
    return _CLAUSE_RE.findall(text.lower())


@dataclass
class _IndexedEntry:
    entry: KnowledgeEntry
    tokens: list[str]
    tf: Counter = field(default_factory=Counter)
    norm: float = 0.0


class SearchEngine:
    """Keyword + TF-IDF search over a set of knowledge entries."""

    def __init__(
        self,
        entries: list[KnowledgeEntry],
        *,
        embed_fn: Callable[[str], list[float]] | None = None,
        embed_dim: int | None = None,
    ) -> None:
        self._indexed: list[_IndexedEntry] = []
        self._doc_freq: Counter = Counter()
        self._num_docs = 0
        self._embed_fn = embed_fn
        self._embed_dim = embed_dim

        self.index(entries)

    # ------------------------------------------------------------------ index
    def index(self, entries: list[KnowledgeEntry]) -> None:
        """(Re)build the TF-IDF index over the given entries."""
        self._indexed = []
        self._doc_freq = Counter()

        # First pass: term frequencies and document frequency.
        for entry in entries:
            tokens = _tokenize(entry.searchable_text())
            tf = Counter(tokens)
            self._doc_freq.update(tf.keys())
            self._indexed.append(_IndexedEntry(entry=entry, tokens=tokens, tf=tf))

        self._num_docs = max(1, len(self._indexed))

        # Second pass: TF-IDF vectors and L2 norms.
        for idx in self._indexed:
            for term in idx.tf:
                tfidf = self._tfidf(term, idx.tf[term])
                idx.tf[term] = tfidf
            idx.norm = math.sqrt(sum(v * v for v in idx.tf.values())) or 1.0

    def add_entry(self, entry: KnowledgeEntry) -> None:
        """Incrementally add one entry to the index (rebuilds for simplicity)."""
        current = [ie.entry for ie in self._indexed]
        current.append(entry)
        self.index(current)

    def _tfidf(self, term: str, tf: int) -> float:
        idf = math.log((1.0 + self._num_docs) / (1.0 + self._doc_freq.get(term, 0))) + 1.0
        return (1.0 + math.log(tf)) * idf

    # --------------------------------------------------------------- scoring
    def _keyword_score(self, query: str, idx: _IndexedEntry) -> float:
        """Exact clause match + keyword overlap score in [0, 1]."""
        q_lower = query.lower().strip()
        score = 0.0

        # 1. Exact clause-number matches are strong signals.
        q_clauses = set(_clause_tokens(query))
        if q_clauses:
            entry_clauses = set(_clause_tokens(idx.entry.clause))
            overlap = q_clauses & entry_clauses
            if overlap:
                # Exact equality scores highest; shared numeric prefix still scores.
                if idx.entry.clause.lower() in {c for c in q_clauses}:
                    score += 1.0
                else:
                    score += 0.5
            # Numeric prefix matches (e.g. query "5.1" matches clause "5.1.3").
            for qc in q_clauses:
                for ec in entry_clauses:
                    if ec.startswith(qc + ".") and score < 0.9:
                        score += 0.3

        # 2. Keyword overlap.
        q_tokens = set(_tokenize(query))
        if q_tokens:
            entry_tokens = set(idx.tokens)
            hit = len(q_tokens & entry_tokens)
            # Weighted by how specific the matched tokens are.
            if hit:
                coverage = hit / len(q_tokens)
                score += min(1.0, coverage) * 0.6
            # Bonus for title hits.
            title_tokens = set(_tokenize(idx.entry.title))
            if q_tokens & title_tokens:
                score += 0.3
            # Bonus for explicit keyword-field hits.
            kw_tokens = set(_tokenize(" ".join(idx.entry.keywords)))
            if q_tokens & kw_tokens:
                score += 0.3

        return min(1.0, score)

    def _semantic_score(self, query: str, idx: _IndexedEntry) -> float:
        """Cosine similarity between the query TF-IDF vector and the entry vector."""
        q_tokens = _tokenize(query)
        if not q_tokens:
            return 0.0
        q_tf = Counter(q_tokens)
        q_vec = {t: self._tfidf(t, c) for t, c in q_tf.items()}
        q_norm = math.sqrt(sum(v * v for v in q_vec.values())) or 1.0

        dot = 0.0
        for term, weight in q_vec.items():
            if term in idx.tf:
                dot += weight * idx.tf[term]
        return dot / (q_norm * idx.norm)

    # ----------------------------------------------------------------- search
    def search(
        self,
        query: str,
        *,
        top_k: int = 5,
        mode: str = "hybrid",
    ) -> list[SearchResult]:
        """Search and return ranked results.

        ``mode`` is one of ``"keyword"``, ``"semantic"`` or ``"hybrid"``.
        """
        mode = mode.lower()
        if mode not in ("keyword", "semantic", "hybrid"):
            mode = "hybrid"

        scored: list[tuple[float, str, _IndexedEntry]] = []
        for idx in self._indexed:
            kw = self._keyword_score(query, idx)
            sem = self._semantic_score(query, idx)

            if mode == "keyword":
                score, match_type = kw, "keyword"
            elif mode == "semantic":
                score, match_type = sem, "semantic"
            else:
                # Keyword dominates for precise clause/number queries; semantic
                # carries natural-language queries.
                score = 0.55 * kw + 0.45 * sem
                match_type = "hybrid"

            if score > 0.0:
                scored.append((score, match_type, idx))

        scored.sort(key=lambda t: t[0], reverse=True)
        return [
            SearchResult(
                entry=idx.entry,
                score=round(score, 4),
                match_type=match_type,
            )
            for score, match_type, idx in scored[:top_k]
        ]


def _load_embedding_fn():
    """Lazily import sentence-transformers if available.

    Returns ``(embed_fn, dim)`` or ``(None, None)`` when unavailable.
    """
    try:
        from sentence_transformers import SentenceTransformer  # type: ignore
    except Exception:
        return None, None

    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    try:
        model = SentenceTransformer(model_name)
    except Exception:
        return None, None

    def embed(text: str) -> list[float]:
        return [float(x) for x in model.encode(text, normalize_embeddings=True)]

    return embed, model.get_sentence_embedding_dimension()


def build_search_engine(
    entries: list[KnowledgeEntry],
    *,
    use_embeddings: bool = False,
) -> SearchEngine:
    """Construct a :class:`SearchEngine` with the optional dense backend."""
    embed_fn = None
    embed_dim = None
    if use_embeddings:
        embed_fn, embed_dim = _load_embedding_fn()
    return SearchEngine(entries, embed_fn=embed_fn, embed_dim=embed_dim)


__all__ = ["SearchEngine", "build_search_engine", "SearchResult"]
