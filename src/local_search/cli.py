"""CLI entry point for local_search."""

from __future__ import annotations

import argparse
import os

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
    fts5_available_check,
    schema_init,
    schema_version_get,
)


ANSI_GREEN = "\033[32m"
ANSI_RED = "\033[31m"
ANSI_BLUE = "\033[34m"
ANSI_YELLOW = "\033[33m"
ANSI_RESET = "\033[0m"


def color_enabled() -> bool:
    """Return True if ANSI colors should be emitted."""
    return os.environ.get("NO_COLOR") is None


def green(text: str) -> str:
    if not color_enabled():
        return text
    return f"{ANSI_GREEN}{text}{ANSI_RESET}"


def red(text: str) -> str:
    if not color_enabled():
        return text
    return f"{ANSI_RED}{text}{ANSI_RESET}"


def color_enabled() -> bool:
    """Return True if ANSI colors should be emitted."""
    return os.environ.get("NO_COLOR") is None


def _color(text: str, ansi: str) -> str:
    if not color_enabled():
        return text
    return f"{ansi}{text}{ANSI_RESET}"


def pass_print(message: str) -> None:
    print(_color(f"[✓] {message}", ANSI_GREEN))


def fail_print(message: str) -> None:
    print(_color(f"[x] {message}", ANSI_RED))


def info_print(message: str) -> None:
    print(_color(f"[*] {message}", ANSI_BLUE))


def debug_print(message: str) -> None:
    print(_color(f"[debug] {message}", ANSI_YELLOW))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="local-search",
        description="Local-first search engine for files and web artifacts.",
    )

    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("status", help="Show local_search status.")
    subparsers.add_parser("doctor", help="Run local_search health checks.")

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


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "status":
        return status_command()

    if args.command == "doctor":
        return doctor_command()

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
