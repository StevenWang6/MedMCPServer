"""Document ingestion: index user-supplied documents into the knowledge base.

Supported file types in the documents directory:

* **.json** — either a JSON array of knowledge-entry objects, or an object with an
  ``"entries"`` array. Each entry accepts: ``id``, ``clause``, ``title``,
  ``content``, ``category``, ``keywords``, ``related``, ``safety_class``.
* **.md / .markdown** — split on Markdown headings; each heading becomes a section
  entry (``#`` → title, the following text → content).
* **.txt** — the whole file becomes a single entry named after the file.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from medmcp.models import KnowledgeEntry

DEFAULT_DOCUMENTS_DIR = Path(__file__).resolve().parent.parent / "data" / "documents"

_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$", re.MULTILINE)
_JSON_SUFFIXES = {".json"}
_MD_SUFFIXES = {".md", ".markdown"}
_TXT_SUFFIXES = {".txt", ".text"}

_SUPPORTED_SUFFIXES = _JSON_SUFFIXES | _MD_SUFFIXES | _TXT_SUFFIXES


class DocumentError(Exception):
    """Raised when a document cannot be parsed."""


def _normalize_entry(data: dict, source: str, fallback_id: str) -> KnowledgeEntry:
    """Coerce a raw dict into a :class:`KnowledgeEntry`, tolerating partial data."""
    content = str(data.get("content") or data.get("description") or "").strip()
    title = str(data.get("title") or data.get("name") or fallback_id).strip()
    clause = str(data.get("clause") or data.get("id") or fallback_id).strip()
    entry_id = str(data.get("id") or clause).strip()

    keywords = data.get("keywords") or []
    if isinstance(keywords, str):
        keywords = [k.strip() for k in keywords.split(",") if k.strip()]
    else:
        keywords = [str(k).strip() for k in keywords if str(k).strip()]

    related = data.get("related") or []
    related = [str(r).strip() for r in related if str(r).strip()]

    category = data.get("category") or "general"
    safety_class = data.get("safety_class")

    return KnowledgeEntry(
        id=entry_id,
        clause=clause,
        title=title,
        content=content,
        category=category,  # type: ignore[arg-type]
        keywords=keywords,
        related=related,
        safety_class=safety_class,  # type: ignore[arg-type]
        source=source,
    )


def _parse_json(path: Path, source: str) -> list[KnowledgeEntry]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        raise DocumentError(f"Invalid JSON in {path.name}: {exc}") from exc

    if isinstance(raw, dict):
        raw = raw.get("entries", [])
    if not isinstance(raw, list):
        raise DocumentError(f"JSON document {path.name} must be an array or an object with 'entries'.")

    entries: list[KnowledgeEntry] = []
    for i, item in enumerate(raw):
        if not isinstance(item, dict):
            continue
        entries.append(_normalize_entry(item, source, f"{path.stem}-{i + 1}"))
    return entries


def _parse_markdown(path: Path, source: str) -> list[KnowledgeEntry]:
    text = path.read_text(encoding="utf-8-sig")
    headings = list(_HEADING_RE.finditer(text))

    if not headings:
        # No headings: fall back to whole-file entry.
        return [
            KnowledgeEntry(
                id=f"{path.stem}-1",
                clause=f"{path.stem}",
                title=path.stem.replace("_", " ").replace("-", " ").title(),
                content=text.strip(),
                source=source,
            )
        ]

    entries: list[KnowledgeEntry] = []
    for i, match in enumerate(headings):
        start = match.end()
        end = headings[i + 1].start() if i + 1 < len(headings) else len(text)
        body = text[start:end].strip()
        title = match.group(2).strip()
        slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
        entries.append(
            KnowledgeEntry(
                id=f"{path.stem}-{slug or i + 1}",
                clause=f"{path.stem}",
                title=title,
                content=body,
                source=source,
            )
        )
    return entries


def _parse_text(path: Path, source: str) -> list[KnowledgeEntry]:
    text = path.read_text(encoding="utf-8-sig").strip()
    return [
        KnowledgeEntry(
            id=f"{path.stem}-1",
            clause=f"{path.stem}",
            title=path.stem.replace("_", " ").replace("-", " ").title(),
            content=text,
            source=source,
        )
    ]


def load_documents(
    directory: str | Path = DEFAULT_DOCUMENTS_DIR,
) -> tuple[list[KnowledgeEntry], list[str]]:
    """Load and parse all supported documents in ``directory``.

    Returns ``(entries, errors)`` where ``errors`` lists per-file problems.
    """
    root = Path(directory)
    if not root.is_dir():
        return [], [f"Documents directory not found: {root}"]

    entries: list[KnowledgeEntry] = []
    errors: list[str] = []

    for path in sorted(root.iterdir()):
        if path.name.startswith(".") or path.name == "README.md":
            continue
        if path.suffix.lower() not in _SUPPORTED_SUFFIXES:
            continue

        source = f"document:{path.name}"
        try:
            if path.suffix.lower() in _JSON_SUFFIXES:
                parsed = _parse_json(path, source)
            elif path.suffix.lower() in _MD_SUFFIXES:
                parsed = _parse_markdown(path, source)
            else:
                parsed = _parse_text(path, source)
            entries.extend(parsed)
        except DocumentError as exc:
            errors.append(str(exc))
        except Exception as exc:  # pragma: no cover - defensive
            errors.append(f"Failed to parse {path.name}: {exc}")

    return entries, errors


__all__ = [
    "DEFAULT_DOCUMENTS_DIR",
    "DocumentError",
    "load_documents",
]
