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

```text
~/local_search/data/local_search