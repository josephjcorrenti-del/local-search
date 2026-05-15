"""Web search fallback helpers for local_search."""

from __future__ import annotations

import json
import os
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import quote_plus
from urllib.request import Request, urlopen

from local_search.config import (
    DEFAULT_SEARXNG_BASE_URL,
    DEFAULT_WEB_SEARCH_PROVIDER,
    WEB_SEARCH_TIMEOUT_SECONDS,
)
from local_search.paths import ARTIFACTS_DIR, WEB_ARTIFACTS_DIR


def normalized_name_build(value: str) -> str:
    """Return a filesystem-friendly normalized name."""
    normalized = value.lower()
    normalized = re.sub(r"[^a-z0-9]+", "_", normalized)
    normalized = normalized.strip("_")
    return normalized or "query"


def artifact_path_build(query: str) -> Path:
    """Build a human-readable web search artifact path."""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    name = normalized_name_build(query)
    return WEB_ARTIFACTS_DIR / f"search_{name}_{timestamp}.json"


def content_text_build(results: list[dict[str, str]]) -> str:
    """Build searchable plain text from structured web results."""
    parts: list[str] = []

    for result in results:
        parts.extend(
            [
                result["title"],
                result["url"],
                result["snippet"],
                "",
            ]
        )

    return "\n".join(parts).strip()


def searxng_results_parse(payload: dict) -> list[dict[str, str]]:
    """Parse SearXNG JSON results into the local_search result contract."""
    results: list[dict[str, str]] = []

    for item in payload.get("results", []):
        title = str(item.get("title") or "").strip()
        url = str(item.get("url") or "").strip()
        snippet = str(item.get("content") or "").strip()

        if not title or not url:
            continue

        results.append(
            {
                "title": title,
                "url": url,
                "snippet": snippet,
            }
        )

    return results


def web_search(query: str) -> dict:
    """Search SearXNG, save structured results, and return them."""
    WEB_ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

    base_url = os.environ.get("LOCAL_SEARCH_SEARXNG_URL", DEFAULT_SEARXNG_BASE_URL)
    search_url = f"{base_url.rstrip('/')}/search?q={quote_plus(query)}&format=json"

    request = Request(
        search_url,
        headers={
            "User-Agent": "local_search/0.1",
            "Accept": "application/json",
        },
    )

    with urlopen(request, timeout=WEB_SEARCH_TIMEOUT_SECONDS) as response:
        content_bytes = response.read()
        content_type = response.headers.get("content-type")

    payload = json.loads(content_bytes.decode("utf-8", errors="replace"))
    results = searxng_results_parse(payload)
    content_text = content_text_build(results)

    artifact_path = artifact_path_build(query)

    artifact = {
        "artifact_type": "web_search_results",
        "provider": DEFAULT_WEB_SEARCH_PROVIDER,
        "query": query,
        "search_url": search_url,
        "fetched_at": datetime.now().astimezone().isoformat(),
        "content_type": content_type,
        "title": f"Search results for {query}",
        "results": results,
        "content_text": content_text,
    }

    artifact_path.write_text(
        json.dumps(artifact, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    return {
        "status": "ok",
        "query": query,
        "results": results,
        "artifact_path": str(artifact_path),
    }