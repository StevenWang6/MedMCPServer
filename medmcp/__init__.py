"""MedMCP — an MCP server for IEC 62304 medical device software knowledge queries."""

__version__ = "0.1.0"

from medmcp.server import build_server, create_server

__all__ = ["__version__", "build_server", "create_server"]
