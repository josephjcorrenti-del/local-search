from __future__ import annotations

"""SQLite storage helpers for local_search."""

import sqlite3
from pathlib import Path
from typing import Any

from local_search.config import SCHEMA_VERSION
from local_search.paths import DB_PATH
from local_search.paths import ensure_app_dirs


def connection_get(db_path: Path = DB_PATH) -> sqlite3.Connection:
    """Return a SQLite connection for the search database."""
    ensure_app_dirs()
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def fts5_available_check() -> bool:
    """Return True when SQLite FTS5 is available."""
    with sqlite3.connect(":memory:") as conn:
        try:
            conn.execute("CREATE VIRTUAL TABLE fts_test USING fts5(content)")
            return True
        except sqlite3.OperationalError:
            return False


def schema_init(db_path: Path = DB_PATH) -> None:
    """Initialize the local_search SQLite schema."""
    with connection_get(db_path) as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS schema_version (
                version INTEGER NOT NULL,
                applied_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS sources (
                source_id TEXT PRIMARY KEY,
                source_type TEXT NOT NULL,
                path TEXT,
                url TEXT,
                title TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                metadata_json TEXT
            );

            CREATE TABLE IF NOT EXISTS documents (
                document_id TEXT PRIMARY KEY,
                source_id TEXT NOT NULL,
                document_type TEXT NOT NULL,
                title TEXT,
                path TEXT,
                url TEXT,
                content_sha256 TEXT NOT NULL,
                size_bytes INTEGER,
                raw_ref TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                indexed_at TEXT,
                metadata_json TEXT,
                FOREIGN KEY(source_id) REFERENCES sources(source_id)
            );

            CREATE TABLE IF NOT EXISTS document_chunks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chunk_id TEXT NOT NULL UNIQUE,
                document_id TEXT NOT NULL,
                chunk_index INTEGER NOT NULL,
                content TEXT NOT NULL,
                start_char INTEGER,
                end_char INTEGER,
                token_count INTEGER,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(document_id) REFERENCES documents(document_id)
            );

            CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5(
                title,
                path,
                url,
                content,
                content='document_chunks',
                content_rowid='id'
            );
            """
        )

        existing = conn.execute("SELECT COUNT(*) FROM schema_version").fetchone()[0]
        if existing == 0:
            conn.execute(
                "INSERT INTO schema_version (version) VALUES (?)",
                (SCHEMA_VERSION,),
            )


def counts_get(db_path: Path = DB_PATH) -> dict[str, int]:
    """Return basic database object counts."""
    if not db_path.exists():
        return {
            "sources": 0,
            "documents": 0,
            "chunks": 0,
        }

    with connection_get(db_path) as conn:
        return {
            "sources": int(conn.execute("SELECT COUNT(*) FROM sources").fetchone()[0]),
            "documents": int(conn.execute("SELECT COUNT(*) FROM documents").fetchone()[0]),
            "chunks": int(conn.execute("SELECT COUNT(*) FROM document_chunks").fetchone()[0]),
        }


def schema_version_get(db_path: Path = DB_PATH) -> int | None:
    """Return the current schema version, if initialized."""
    if not db_path.exists():
        return None

    with connection_get(db_path) as conn:
        row: Any = conn.execute(
            "SELECT version FROM schema_version ORDER BY applied_at DESC LIMIT 1"
        ).fetchone()

    if row is None:
        return None

    return int(row["version"])
