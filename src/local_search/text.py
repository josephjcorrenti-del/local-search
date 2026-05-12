from __future__ import annotations

"""Text helpers for local_search."""

import hashlib


def sha256_hex(text: str) -> str:
    """Return SHA256 hex digest for text."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def chunk_text(
    text: str,
    *,
    chunk_size: int = 1200,
    chunk_overlap: int = 200,
) -> list[dict]:
    """Split text into overlapping character chunks."""
    chunks: list[dict] = []

    if not text.strip():
        return chunks

    start = 0
    chunk_index = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))
        content = text[start:end]

        chunks.append(
            {
                "chunk_index": chunk_index,
                "content": content,
                "start_char": start,
                "end_char": end,
            }
        )

        if end >= len(text):
            break

        start += chunk_size - chunk_overlap
        chunk_index += 1

    return chunks
