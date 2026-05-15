from pathlib import Path

from local_search.cli import index_file_command
from local_search.storage import schema_init, search_get


def test_search_returns_indexed_file(tmp_path: Path) -> None:
    schema_init()

    sample = tmp_path / "sample.txt"
    sample.write_text(
        f"unique sqlite search test content alpha bravo {tmp_path}\n",
        encoding="utf-8",
    )

    index_file_command(str(sample))

    results = search_get("alpha", limit=10)

    assert len(results) >= 1
    assert results[0]["source_type"] == "file"
    assert results[0]["index_path"] == str(sample.resolve())
    assert "alpha" in results[0]["snippet"].lower()


def test_search_missing_term_returns_empty_list(tmp_path: Path) -> None:
    schema_init()

    sample = tmp_path / "sample.txt"
    sample.write_text(
        f"unique missing term test content charlie delta {tmp_path}\n",
        encoding="utf-8",
    )

    index_file_command(str(sample))

    results = search_get("nonexistentterm", limit=10)

    assert results == []
