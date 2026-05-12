local_search - v1 minimal usable search

Project setup
[ ] create project skeleton
[ ] create src/local_search package
[ ] add pyproject.toml
[ ] add docs/decisions.md
[ ] add docs/todo-list.md
[ ] add scripts/tests directory
[ ] define data root: ~/ai/data/local_search
[ ] define DB path: ~/ai/data/local_search/search.db
[ ] define log path: ~/ai/data/local_search/logs/run.log

Core modules
[ ] add config.py
[ ] add logging.py
[ ] add storage.py
[ ] add documents.py
[ ] add ingest.py
[ ] add query.py
[ ] add ranking.py
[ ] add cli.py

Logging
[ ] implement NDJSON log_event
[ ] write logs to stdout
[ ] duplicate logs to ~/ai/data/local_search/logs/run.log
[ ] include ts, level, event, command, run_id, event_outcome, elapsed_ms, error
[ ] keep human CLI output separate from structured logs

Database
[ ] initialize SQLite database
[ ] enable/use FTS5
[ ] create sources table
[ ] create documents table
[ ] create document_chunks table
[ ] create chunks_fts virtual table
[ ] add schema version table

Index file
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

Index web artifact
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

Search
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

Inspect
[ ] implement inspect-document DOC_ID
[ ] show document metadata
[ ] show source metadata
[ ] show raw_ref
[ ] show chunk count
[ ] optionally show chunks with --chunks
[ ] log document.inspect.start
[ ] log document.inspect.done

Status and doctor
[ ] implement status
[ ] show data root
[ ] show DB path
[ ] show log path
[ ] show document count
[ ] show chunk count
[ ] show source counts
[ ] implement doctor
[ ] check data root exists
[ ] check DB exists or can be created
[ ] check FTS5 is available
[ ] check log path is writable
[ ] emit doctor.check.ok
[ ] emit doctor.check.fail

Tests
[ ] add pytest tests for schema initialization
[ ] add pytest tests for index-file
[ ] add pytest tests for unchanged file skip
[ ] add pytest tests for search returns ranked results
[ ] add pytest tests for inspect-document
[ ] add bash smoke test for status
[ ] add bash smoke test for doctor
[ ] add bash smoke test for index-file + search

Deferrals
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
