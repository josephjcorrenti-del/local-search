## Rules

- Easy first, then top down.

## Roadmap

local_search - v1 minimal usable search

## Project setup
[x] create project skeleton
[x] create src/local_search package
[x] add pyproject.toml
[x] add docs/decisions.md
[x] add docs/todo-list.md
[x] add scripts/tests directory
[x] define data root: data/local_search
[x] define DB path: data/local_search/search.db
[x] define log path: data/local_search/logs/run.log
[x] initialize git
[x] create GitHub repo
[x] create virtual environment
[x] configure editable install
[x] create baseline pytest setup
[x] create baseline smoke test runner
[x] add .gitignore

## Core modules
[x] add config.py
[x] add log.py
[x] add storage.py
[x] add documents.py
[x] add ingest.py
[x] add query.py
[x] add ranking.py
[x] add cli.py
[x] add paths.py
[x] add text.py
[x] add output.py

## Logging
[x] implement NDJSON log_event
[x] write logs to stdout when LOCAL_SEARCH_VERBOSE=1
[x] duplicate logs to data/local_search/logs/run.log
[x] include ts, level, event, command, run_id, event_outcome, elapsed_ms, error
[x] keep human CLI output separate from structured logs
[x] wire local_search logs into ELK/Filebeat
[x] verify local_search logs in Kibana

## Database
[x] initialize SQLite database
[x] enable/use FTS5
[x] add SCHEMA_VERSION
[x] create schema_version table
[x] create sources table
[x] create documents table
[x] create document_chunks table
[x] create chunks_fts virtual table

## Index file
[x] implement index-file PATH
[x] validate path exists
[x] validate path is a file
[x] read plain text files only for v1
[x] compute sha256 hash of content
[x] skip unchanged files
[x] create source record
[x] create document record
[x] chunk content by simple character window
[x] store chunks in document_chunks
[x] insert searchable text into chunks_fts
[x] log index.file.start
[x] log index.file.done
[x] log index.file.skip_unchanged
[x] log index.file.error

## Index web artifact
[ ] implement index-web-artifact PATH
[ ] validate artifact path exists
[ ] support ollama_workbench web artifact JSON
[ ] extract url when present
[ ] extract title when present
[ ] extract content/text when present
[ ] store original artifact path as raw_ref
[ ] compute sha256 hash of extracted content
[ ] skip unchanged artifacts
[ ] create source record
[ ] create document record
[ ] chunk extracted content
[ ] insert chunks into FTS index
[ ] log index.web_artifact.start
[ ] log index.web_artifact.done
[ ] log index.web_artifact.error

## Search
[x] implement search QUERY
[x] use SQLite FTS5 MATCH
[x] rank results with BM25
[x] return document_id
[x] return chunk_id
[x] return source_type
[x] return path when available
[x] return url when available
[x] return title when available
[x] return snippet
[x] return score
[x] support --limit
[x] support --json
[x] log search.query.start
[x] log search.query.done
[ ] log search.query.error

## Inspect
[x] implement inspect-document DOC_ID
[x] show document metadata
[x] show source metadata
[x] show raw_ref
[x] show chunk count
[ ] optionally show chunks with --chunks
[x] log document.inspect.start
[x] log document.inspect.done

## Status and doctor
[x] implement status
[x] show data root
[x] show DB path
[x] show log path
[x] show document count
[x] show chunk count
[x] show source counts
[x] implement doctor
[x] check data root exists
[x] check DB exists or can be created
[x] check FTS5 is available
[x] check log path is writable
[x] emit doctor.check.ok
[x] emit doctor.check.fail
[x] add colored pass/fail/info/debug CLI helpers

## Completed infrastructure
[x] GitHub repo created
[x] GitHub Actions running
[x] ELK/Filebeat configured
[x] local_search logs visible in Kibana

## Path to index path
[x] rename sources.path to sources.index_path
[x] rename documents.path to documents.index_path
[x] rename chunks_fts.path to chunks_fts.index_path
[x] update storage helpers for index_path
[x] update tests for index_path

## Smart search
[ ] make unknown/default args become search query
[ ] keep explicit subcommands working
[ ] add --local-only
[ ] add --web-only later
[x] add web fallback placeholder first
[ ] then implement real web search artifact creation

## Useful data file names

## Tests
[x] add pytest tests for schema initialization
[x] add pytest tests for index-file
[x] add pytest tests for unchanged file skip
[x] add pytest tests for search returns ranked results
[x] add pytest tests for inspect-document
[x] add bash smoke test for status
[x] add bash smoke test for doctor
[x] add bash smoke test for index-file + search
[x] add GitHub Actions test workflow
[x] verify GitHub Actions passing

## Refactors
[x] move index-file ingest workflow from cli.py to ingest.py
[x] move CLI color/output helpers from cli.py to output.py
[x] keep cli.py focused on orchestration

## to be prioritized (tpb)
[ ] clear all history
[ ] all objects need human readable names <object_type>_<normalized_name>_<yyyymmddhhmmss>.<ext>

### Duplicate handling
[ ] define duplicate behavior for identical content from different sources
[ ] define duplicate behavior for identical URLs with changed content
[ ] define duplicate behavior for renamed artifacts with identical content
[ ] define whether duplicate chunks should be stored or reused
[ ] define inspect/debug visibility for duplicate detection
[ ] define whether source_id or document_id is canonical for dedupe

## Deferrals
[ ] defer shell component
[ ] defer embeddings
[ ] defer vector database
[ ] defer crawler
[ ] defer web UI
[ ] defer background indexing daemon
[ ] defer AI summarization
[ ] defer tight ollama_workbench coupling
[ ] defer HTTP API
[ ] defer advanced permissions
