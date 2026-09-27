import pytest
from pathlib import Path
from typing import List, Dict

from HGNCapp import data_filtering

# ------------------------------------------------------------------
# read_file tests
# ------------------------------------------------------------------

def test_read_file_happy(tmp_path: Path) -> None:
    """Test reading valid file with multiple entries."""
    file = tmp_path / "test.tsv"
    file.write_text(
        "hgnc_id\tHEADER2\tHEADER3\tHEADER4\n"
        "GENE1\tTX1\t1.1\t0.2\n"
        "GENE2\tTX2\t2.2\t0.3\n"
    )

    result = data_filtering.read_file(file)

    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["hgnc_id"] == "GENE1"
    assert result[1]["hgnc_id"] == "GENE2"


def test_read_file_skips_invalid_lines(tmp_path: Path) -> None:
    """Malformed lines should be skipped, not crash."""
    file = tmp_path / "test.tsv"
    file.write_text(
        "hgnc_id\tHEADER2\tHEADER3\tHEADER4\n"
        "GENE1\tTX1\t1.1\t0.2\n"
        "BADLINE\n"
        "GENE2\tTX2\t2.2\t0.3\n"
    )

    result = data_filtering.read_file(file)

    assert len(result) == 2


def test_read_file_all_invalid(tmp_path: Path) -> None:
    """All invalid lines should raise ValueError."""
    file = tmp_path / "test.tsv"
    file.write_text("BADLINE\nBADLINE2\n")

    with pytest.raises(ValueError):
        data_filtering.read_file(file)


def test_read_file_missing_file(tmp_path: Path) -> None:
    """Non-existent file should raise an error."""
    file = tmp_path / "does_not_exist.tsv"

    with pytest.raises(Exception):
        data_filtering.read_file(file)