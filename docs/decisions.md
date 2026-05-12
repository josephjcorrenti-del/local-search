# local_search Decisions

## 2026-05-11 - Project purpose

`local_search` is a local-first search engine for personal files and saved web artifacts.

It should work independently as a search tool and may later be used by `ollama_workbench`, but it should not be tightly coupled to AI workflows in v1.

## 2026-05-11 - Language

Use Python for v1.

Reasons:
- consistent with `ollama_workbench`
- fast to build and test
- built-in SQLite support
- simple CLI and pytest workflow
- enough performance for local-first v1

## 2026-05-11 - Storage

Use SQLite with FTS5 for v1.

Reasons:
- local single-file database
- inspectable
- no server dependency
- supports full-text search
- supports useful ranking with BM25
- easy to rebuild from raw sources

## 2026-05-11 - Data root

Use:

~/local_search/data/local_search

Reasons:
- keeps v1 self-contained in the project repo
- easy to inspect during development
- avoids writing into broader ~/ai project data until integration is earned

All filesystem locations should live in paths.py.

## 2026-05-11 - Deterministic IDs

Use deterministic IDs as the master contract:

src_<sha256>
doc_<sha256>
chunk_<docid>_<index>

Rules:
- source IDs derive from stable source identity
- document IDs derive from content identity
- chunk IDs derive from document ID plus chunk index
- avoid random UUIDs for indexed objects

## 2026-05-11 - Raw vs processed data

Raw source data remains canonical.

The search index is processed, disposable, and rebuildable.

## 2026-05-11 - CLI-first design

Initial commands:
- status
- doctor
- index-file
- index-web-artifact
- search
- inspect-document

## 2026-05-11 - No shell in v1

Do not add an interactive shell in v1.

## 2026-05-11 - No tight AI coupling in v1

local_search should not call Ollama or know about ollama_workbench sessions in v1.

Future integration should happen through a clear CLI/JSON boundary.

## 2026-05-11 - Logging and observability

Use structured NDJSON logs.

Logs should go to:
- stdout
- ~/local_search/data/local_search/logs/run.log

## 2026-05-11 - Schema versioning

Use:
SCHEMA_VERSION = 1

A schema_version table should exist from the beginning.

## 2026-05-11 - Deferrals

Do not implement these in v1:
- embeddings
- vector database
- crawler
- web UI
- HTTP API
- background indexing daemon
- AI summarization
- interactive shell
- tight ollama_workbench coupling