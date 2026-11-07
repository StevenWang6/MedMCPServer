"""Command-line entry points for the MedMCP server.

Subcommands:

    stdio   Run over stdio (default; for local MCP clients such as Claude/Copilot).
    sse     Run an HTTP + SSE server (``--host``/``--port``).
    http    Run a streamable-HTTP server (``--host``/``--port``).
"""

from __future__ import annotations

import argparse
import sys

from medmcp.server import build_server


def _add_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--docs",
        default=None,
        help="Documents directory to index (default: data/documents).",
    )
    parser.add_argument(
        "--embeddings",
        action="store_true",
        help="Use sentence-transformers embeddings for semantic search (if installed).",
    )
    parser.add_argument(
        "--index-on-startup",
        action="store_true",
        help="Index documents at startup (same as MEDMCP_INDEX_ON_STARTUP=1).",
    )


def _add_host_port(parser: argparse.ArgumentParser, default_port: int) -> None:
    parser.add_argument("--host", default="127.0.0.1", help="Bind host (default: 127.0.0.1).")
    parser.add_argument("--port", type=int, default=default_port, help="Bind port.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="medmcp",
        description="IEC 62304 medical device software knowledge MCP server.",
    )
    sub = parser.add_subparsers(dest="command")

    p_stdio = sub.add_parser("stdio", help="Run over stdio (default).")
    _add_common(p_stdio)

    p_sse = sub.add_parser("sse", help="Run an HTTP + SSE server.")
    _add_common(p_sse)
    _add_host_port(p_sse, 8000)
    p_sse.add_argument("--mount-path", default=None, help="Optional SSE mount path.")

    p_http = sub.add_parser("http", help="Run a streamable-HTTP server.")
    _add_common(p_http)
    _add_host_port(p_http, 8000)

    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    command = args.command or "stdio"

    mcp = build_server(
        documents_dir=args.docs,
        use_embeddings=args.embeddings,
        index_on_startup=args.index_on_startup or None,
        host=getattr(args, "host", "127.0.0.1"),
        port=getattr(args, "port", 8000),
    )

    if command == "stdio":
        mcp.run(transport="stdio")
    elif command == "sse":
        mcp.run(transport="sse", mount_path=args.mount_path)
    elif command == "http":
        mcp.run(transport="streamable-http")
    else:  # pragma: no cover - argparse guards this
        print(f"Unknown command: {command}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
