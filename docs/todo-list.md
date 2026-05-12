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
[ ] add storage.py
[x] add documents.py
[x] add ingest.py
[x] add query.py
[x] add ranking.py
[x] add cli.py
[x] add paths.py
[x] add text.py

## Logging
[x] implement NDJSON log_event
[x] write logs to stdout when LOCAL_SEARCH_VERBOSE=1
[x] duplicate logs to data/local_search/logs/run.log
[x] include ts, level, event, command, run_id, event_outcome, elapsed_ms, error
[x] keep human CLI output separate from structured logs
[x] wire local_search logs into ELK/Filebeat
[x] verify local_search logs in Kibana

## Database
[ ] initialize SQLite database
[ ] enable/use FTS5
[ ] add SCHEMA_VERSION
[ ] create schema_version table
[ ] create sources table
[ ] create documents table
[ ] create document_chunks table
[ ] create chunks_fts virtual table

## Index file
[ ] implement index-file PATH
[ ] validate path exists
[ ] validate path is a file
[ ] read plain text files only for v1
[ ] compute sha256 hash of content
[ ] skip unchanged files
[ ] create source record
[ ] create document record
[ ] chunk content by simple character window
[ ] store chunks in document_chunks
[ ] insert searchable text into chunks_fts
[ ] log index.file.start
[ ] log index.file.done
[ ] log index.file.skip_unchanged
[ ] log index.file.error

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
[ ] implement search QUERY
[ ] use SQLite FTS5 MATCH
[ ] rank results with BM25
[ ] return document_id
[ ] return chunk_id
[ ] return source_type
[ ] return path when available
[ ] return url when available
[ ] return title when available
[ ] return snippet
[ ] return score
[ ] support --limit
[ ] support --json
[ ] log search.query.start
[ ] log search.query.done
[ ] log search.query.error

## Inspect
[ ] implement inspect-document DOC_ID
[ ] show document metadata
[ ] show source metadata
[ ] show raw_ref
[ ] show chunk count
[ ] optionally show chunks with --chunks
[ ] log document.inspect.start
[ ] log document.inspect.done

## Status and doctor
[x] implement status
[x] show data root
[x] show DB path
[x] show log path
[ ] show document count
[ ] show chunk count
[ ] show source counts
[x] implement doctor
[x] check data root exists
[ ] check DB exists or can be created
[ ] check FTS5 is available
[x] check log path is writable
[x] emit doctor.check.ok
[x] emit doctor.check.fail
[x] add colored pass/fail/info/debug CLI helpers

## Completed infrastructure

[x] GitHub repo created
[x] GitHub Actions running
[x] ELK/Filebeat configured
[x] local_search logs visible in Kibana

## Tests
[ ] add pytest tests for schema initialization
[ ] add pytest tests for index-file
[ ] add pytest tests for unchanged file skip
[ ] add pytest tests for search returns ranked results
[ ] add pytest tests for inspect-document
[x] add bash smoke test for status
[x] add bash smoke test for doctor
[ ] add bash smoke test for index-file + search
[x] add GitHub Actions test workflow
[x] verify GitHub Actions passing

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
