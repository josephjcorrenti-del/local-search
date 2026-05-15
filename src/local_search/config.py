"""Configuration values for local_search."""

from __future__ import annotations

SCHEMA_VERSION = 1

APP_NAME = "local_search"

DEFAULT_CHUNK_SIZE = 1200
DEFAULT_CHUNK_OVERLAP = 200

DEFAULT_SEARCH_LIMIT = 10

DEFAULT_SEARXNG_BASE_URL = "http://localhost:8080"
DEFAULT_WEB_SEARCH_PROVIDER = "searxng"
WEB_SEARCH_TIMEOUT_SECONDS = 20