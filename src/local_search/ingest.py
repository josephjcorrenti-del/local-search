"""Document ingest helpers for local_search."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from local_search.log import log_event
from local_search.storage import (
    chunk_insert,
    document_exists,
    document_insert,
    source_upsert,
)
from local_search.text import chunk_text, sha256_hex


def file_index(path: Path) -> dict[str, Any]:
    """Index a local text file and return a structured ingest result."""
    log_event(
        "index.file.start",
        command="index-file",
        path=str(path),
    )

    if not path.exists():
        log_event(
            "index.file.error",
            command="index-file",
            path=str(path),
            event_outcome="failure",
            error_message="file does not exist",
        )
        return {
            "status": "missing",
            "index_path": str(path),
        }

    if not path.is_file():
        log_event(
            "index.file.error",
            command="index-file",
            path=str(path),
            event_outcome="failure",
            error_message="not a file",
        )
        return {
            "status": "not_file",
            "index_path": str(path),
        }

    resolved_path = path.resolve()
    text = path.read_text(encoding="utf-8")
    content_sha256 = sha256_hex(text)

    if document_exists(content_sha256):
        log_event(
            "index.file.skip_unchanged",
            command="index-file",
            path=str(path),
            event_outcome="success",
        )
        return {
            "status": "unchanged",
            "index_path": str(path),
            "content_sha256": content_sha256,
        }

    source_id = f"src_{sha256_hex(str(resolved_path))}"
    document_id = f"doc_{content_sha256}"

    source_upsert(
        source_id=source_id,
        source_type="file",
        index_path=str(resolved_path),
    )

    document_insert(
        document_id=document_id,
        source_id=source_id,
        document_type="text",
        index_path=str(resolved_path),
        raw_ref=str(resolved_path),
        content_sha256=content_sha256,
        size_bytes=path.stat().st_size,
    )

    chunks = chunk_text(text)

    for chunk in chunks:
        chunk_id = f"chunk_{document_id}_{chunk['chunk_index']}"

        chunk_insert(
            chunk_id=chunk_id,
            document_id=document_id,
            chunk_index=chunk["chunk_index"],
            content=chunk["content"],
            start_char=chunk["start_char"],
            end_char=chunk["end_char"],
            index_path=str(resolved_path),
        )

    log_event(
        "index.file.done",
        command="index-file",
        path=str(path),
        document_id=document_id,
        source_id=source_id,
        event_outcome="success",
    )

    return {
        "status": "indexed",
        "index_path": str(path),
        "resolved_index_path": str(resolved_path),
        "document_id": document_id,
        "source_id": source_id,
        "content_sha256": content_sha256,
        "chunk_count": len(chunks),
    }