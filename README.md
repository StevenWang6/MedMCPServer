# MedMCPServer

[![CI](https://github.com/StevenWang6/MedMCPServer/actions/workflows/ci.yml/badge.svg)](https://github.com/StevenWang6/MedMCPServer/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)

一个提供 **IEC 62304 医疗器械软件生命周期知识查询服务** 的 MCP（Model Context
Protocol）服务器。它内置了 IEC 62304 标准的条款、要求和核心概念，并支持接入你自己的
文档，通过关键词检索 + 语义检索（TF-IDF，可选嵌入模型）进行查询。

> ⚠️ **合规提示**：本知识库是对 IEC 62304 结构化的学习/导航性总结，**不能替代标准
> 规范性原文**。医疗器械组织应依据正式发布的标准文本及其适用监管框架实施相关流程。

## 功能特性

- 📚 **内置知识库**：IEC 62304 第 1~9 章全部条款与子条款、软件安全分级（A/B/C）、
  SOUP、可追溯性、V 模型等核心概念，共 100+ 条目。
- 🔎 **双重检索**：
  - `keyword`：条款号精确匹配 + 关键词命中；
  - `semantic`：纯 Python TF-IDF 余弦相似度（零额外依赖），可选接入
    `sentence-transformers` 嵌入模型；
  - `hybrid`：两者加权融合（默认）。
- 📄 **文档接入**：将 JSON / Markdown / 纯文本文件放入 `data/documents/` 即可扩展知识库。
- 🔌 **双传输协议**：`stdio`（本地客户端）与 HTTP + SSE / streamable HTTP（网络服务）。

## 环境要求

- Python ≥ 3.10（已在 3.14 上验证）
- `mcp` ≥ 1.0、`pydantic` ≥ 2.0（SSE 需 `starlette` + `uvicorn`）

## 安装

```powershell
cd D:\project\MedMCPServer
pip install -e .

# 可选：真实语义嵌入（需要 torch 对应 Python 版本的 wheel）
pip install -e ".[embeddings]"

# 可选：HTTP/SSE 传输（starlette + uvicorn）
pip install -e ".[http]"
```

## 使用

### 1. stdio（本地 MCP 客户端）

```powershell
medmcp stdio
# 或
python -m medmcp stdio
```

### 2. HTTP + SSE（网络服务）

```powershell
medmcp sse --host 0.0.0.0 --port 8000
```

### 3. Streamable HTTP

```powershell
medmcp http --host 127.0.0.1 --port 8000
```

常用参数：

| 参数 | 说明 |
|------|------|
| `--docs <dir>` | 指定文档目录（默认 `data/documents`） |
| `--embeddings` | 使用 `sentence-transformers` 嵌入模型做语义检索 |
| `--index-on-startup` | 启动时索引文档（等价 `MEDMCP_INDEX_ON_STARTUP=1`） |

### 4. 配置到 MCP 客户端

以 Claude Desktop（`claude_desktop_config.json`）为例：

```json
{
  "mcpServers": {
    "medmcp": {
      "command": "python",
      "args": ["-m", "medmcp", "stdio"],
      "cwd": "D:\\project\\MedMCPServer"
    }
  }
}
```

## MCP 工具

| 工具 | 说明 |
|------|------|
| `search_62304(query, mode, top_k, include_related)` | 混合检索。`mode` ∈ `keyword` / `semantic` / `hybrid` |
| `get_clause(clause, include_related)` | 按条款号/概念精确查询（如 `5.1.3`、`4.3`、`SOUP`），未命中时返回建议 |
| `list_clauses(category, query)` | 列出条款，可按类别/文本过滤 |
| `safety_class_info(safety_class)` | 查询 A/B/C 软件安全分级定义与适用条款 |
| `index_documents(directory)` | （重新）索引文档并刷新检索 |
| `list_documents()` | 列出已索引文档 |

## MCP 资源

- `medmcp://knowledge` — 完整知识库（JSON）
- `medmcp://clause/{clause}` — 单条条款（JSON）

## 文档接入格式

放入 `data/documents/` 的文档会被 `index_documents` 索引。支持三种格式：

### JSON（`.json`）

数组或含 `entries` 字段的对象，每项支持：

```json
[
  {
    "id": "ext-1",
    "clause": "annex-a",
    "title": "示例要求",
    "content": "关于软件验证的自定义要求内容。",
    "category": "development",
    "keywords": ["verification", "示例"],
    "related": ["5.5.5"],
    "safety_class": null
  }
]
```

### Markdown（`.md` / `.markdown`）

按标题切分为章节，每个标题成为一条知识条目（标题 → `title`，正文 → `content`）。

### 纯文本（`.txt`）

整个文件作为单条知识条目（文件名 → `title`）。

## 软件安全分级（IEC 62304 第 4.3 条）

| 分级 | 含义 | 适用要点 |
|------|------|----------|
| **A** | 软件故障不会造成伤害或健康损害 | 基本文档与验证 |
| **B** | 软件故障可能导致非严重伤害 | 更严格的文档与验证 |
| **C** | 软件故障可能导致死亡或严重伤害 | 最严格的文档与验证，必须实施第 7 章软件风险管理 |

## 项目结构

```
MedMCPServer/
├── medmcp/
│   ├── __init__.py       # 包入口
│   ├── models.py         # Pydantic 数据模型
│   ├── knowledge.py      # 内置 IEC 62304 知识库
│   ├── search.py         # 关键词 + TF-IDF 语义检索引擎
│   ├── documents.py      # 文档加载/解析
│   ├── server.py         # FastMCP 服务器与工具/资源
│   ├── transport.py      # stdio / SSE / HTTP 命令行入口
│   └── __main__.py       # python -m medmcp
├── data/documents/       # 自定义文档目录
├── tests/test_search.py  # 单元测试
└── pyproject.toml
```

## 运行测试

```powershell
cd D:\project\MedMCPServer
pip install -e ".[dev]"
pytest -q
```

## 许可

MIT
