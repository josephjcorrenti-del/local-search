"""CLI entry point for local_search."""

from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="local-search",
        description="Local-first search engine for files and web artifacts.",
    )

    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("status", help="Show local_search status.")
    subparsers.add_parser("doctor", help="Run local_search health checks.")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "status":
        print("local_search status: not implemented yet")
        return 0

    if args.command == "doctor":
        print("local_search doctor: not implemented yet")
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())