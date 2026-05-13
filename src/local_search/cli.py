"""CLI entry point for local_search."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from local_search.ingest import file_index
from local_search.log import log_event
from local_search.paths import (
    ARTIFACTS_DIR,
    DATA_ROOT,
    DB_PATH,
    EXPORTS_DIR,
    LOG_DIR,
    RUN_LOG,
    ensure_app_dirs,
)
from local_search.storage import (
    counts_get,
    document_inspect_get,
    fts5_available_check,
    schema_init,
    schema_version_get,
    search_get,
)
from local_search.output import (
    info_print,
    pass_print,
    fail_print,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="local-search",
        description="Local-first search engine for files and web artifacts.",
    )

    subparsers = parser.add_subparsers(dest="command")

    status_parser = subparsers.add_parser("status", help="Show local_search status.")
    status_parser.set_defaults(handler=lambda args: status_command())

    doctor_parser = subparsers.add_parser("doctor", help="Run local_search health checks.")
    doctor_parser.set_defaults(handler=lambda args: doctor_command())

    index_file_parser = subparsers.add_parser(
        "index-file",
        help="Index a local text file.",
    )
    index_file_parser.add_argument("path")
    index_file_parser.set_defaults(handler=lambda args: index_file_command(args.path))

    search_parser = subparsers.add_parser(
        "search",
        help="Search indexed content.",
    )
    search_parser.add_argument("query")
    search_parser.add_argument("--limit", type=int, default=10)
    search_parser.add_argument("--json", action="store_true")
    search_parser.set_defaults(
        handler=lambda args: search_command(
            args.query,
            limit=args.limit,
            json_output=args.json,
        )
    )

    inspect_parser = subparsers.add_parser(
        "inspect-document",
        help="Inspect an indexed document.",
    )
    inspect_parser.add_argument("document_id")
    inspect_parser.set_defaults(
        handler=lambda args: inspect_document_command(args.document_id)
    )

    return parser


def status_command() -> int:
    ensure_app_dirs()

    log_event("status.start", command="status")

    info_print("local_search status")
    print()
    info_print("paths")
    info_print(f"  data_root:     {DATA_ROOT}")
    info_print(f"  db_path:       {DB_PATH}")
    info_print(f"  log_dir:       {LOG_DIR}")
    info_print(f"  run_log:       {RUN_LOG}")
    info_print(f"  artifacts_dir: {ARTIFACTS_DIR}")
    info_print(f"  exports_dir:   {EXPORTS_DIR}")
    print()
    info_print("storage")
    info_print(f"  db_exists:     {DB_PATH.exists()}")
    info_print(f"  run_log_exists:{RUN_LOG.exists()}")

    counts = counts_get()
    schema_version = schema_version_get()

    info_print(f"schema_version: {schema_version}")
    info_print(f"sources:        {counts['sources']}")
    info_print(f"documents:      {counts['documents']}")
    info_print(f"chunks:         {counts['chunks']}")

    log_event("status.done", command="status", event_outcome="success")
    return 0


def doctor_command() -> int:
    ensure_app_dirs()

    log_event("doctor.start", command="doctor")

    try:
        schema_init()
        db_ok = DB_PATH.exists()
    except Exception as exc:
        db_ok = False
        log_event(
            "doctor.db.error",
            command="doctor",
            event_outcome="failure",
            error_message=str(exc),
            error_type=type(exc).__name__,
        )

    fts5_ok = fts5_available_check()

    checks = [
        ("data_root exists", DATA_ROOT.exists()),
        ("log_dir exists", LOG_DIR.exists()),
        ("artifacts_dir exists", ARTIFACTS_DIR.exists()),
        ("exports_dir exists", EXPORTS_DIR.exists()),
        ("log_dir writable", LOG_DIR.exists() and LOG_DIR.is_dir()),
        ("db exists or can be created", db_ok),
        ("FTS5 is available", fts5_ok),
    ]

    failed = False

    info_print("local_search doctor")
    print()

    for label, ok in checks:
        if ok:
            pass_print(label)
            log_event(
                "doctor.check.ok",
                command="doctor",
                event_outcome="success",
                path=str(DATA_ROOT),
            )
        else:
            failed = True
            fail_print(label)
            log_event(
                "doctor.check.fail",
                command="doctor",
                event_outcome="failure",
                error_message=label,
            )

    if failed:
        log_event("doctor.done", command="doctor", event_outcome="failure")
        return 1

    print()
    pass_print("doctor passed")
    log_event("doctor.done", command="doctor", event_outcome="success")
    return 0


def index_file_command(path_str: str) -> int:
    result = file_index(Path(path_str))

    if result["status"] == "missing":
        fail_print(f"file does not exist: {result['path']}")
        return 1

    if result["status"] == "not_file":
        fail_print(f"not a file: {result['path']}")
        return 1

    if result["status"] == "unchanged":
        info_print("unchanged file skipped")
        return 0

    pass_print(f"indexed {result['path']}")
    info_print(f"chunks: {result['chunk_count']}")
    return 0


def search_command(query: str, *, limit: int, json_output: bool) -> int:
    log_event(
        "search.query.start",
        command="search",
        query=query,
    )

    results = search_get(query, limit=limit)

    log_event(
        "search.query.done",
        command="search",
        query=query,
        event_outcome="success",
        result_count=len(results),
    )

    if json_output:
        print(json.dumps(results, indent=2))
        return 0

    info_print(f"results for: {query}")
    print()

    if not results:
        info_print("no results")
        return 0

    for index, result in enumerate(results, start=1):
        print(f"{index}. {result['path'] or result['url']}")
        print(f"   score: {result['score']}")
        print(f"   source: {result['source_type']}")
        print(f"   document_id: {result['document_id']}")
        print(f"   chunk_id: {result['chunk_id']}")
        print(f"   snippet: {result['snippet']}")
        print()

    return 0


def inspect_document_command(document_id: str) -> int:
    log_event(
        "document.inspect.start",
        command="inspect-document",
        document_id=document_id,
    )

    result = document_inspect_get(document_id)

    if result is None:
        fail_print(f"document not found: {document_id}")
        log_event(
            "document.inspect.done",
            command="inspect-document",
            document_id=document_id,
            event_outcome="failure",
            error_message="document not found",
        )
        return 1

    document = result["document"]
    chunks = result["chunks"]

    info_print("document")
    info_print(f"  document_id:    {document['document_id']}")
    info_print(f"  source_id:      {document['source_id']}")
    info_print(f"  source_type:    {document['source_type']}")
    info_print(f"  document_type:  {document['document_type']}")
    info_print(f"  path:           {document['path']}")
    info_print(f"  url:            {document['url']}")
    info_print(f"  raw_ref:        {document['raw_ref']}")
    info_print(f"  content_sha256: {document['content_sha256']}")
    info_print(f"  size_bytes:     {document['size_bytes']}")
    info_print(f"  created_at:     {document['created_at']}")
    info_print(f"  indexed_at:     {document['indexed_at']}")
    print()

    info_print("chunks")
    info_print(f"  chunk_count:    {len(chunks)}")

    for chunk in chunks:
        info_print(
            f"  {chunk['chunk_index']}: "
            f"{chunk['chunk_id']} "
            f"chars={chunk['start_char']}-{chunk['end_char']} "
            f"content_chars={chunk['content_chars']}"
        )

    log_event(
        "document.inspect.done",
        command="inspect-document",
        document_id=document_id,
        event_outcome="success",
    )

    return 0


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    handler = getattr(args, "handler", None)
    if handler is None:
        parser.print_help()
        return 0

    return handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
