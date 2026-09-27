import sys
import logging
import csv
import json
from pathlib import Path
from typing import List, Dict, Optional

from HGNCapp.logger import setup_logging

logger = logging.getLogger(__name__)

def read_file(filename: Path) -> List[Dict[str, str]]:
    """
    Read a gnomAD constraint file into a structured list of dictionaries.

    Each line in the input file is parsed into a dictionary with fields:
    gene, transcript, mis_z, and loeuf.

    Parameters
    ----------
    filename : Path
        Path to the input CSV file.

    Returns
    -------
    list of dict
        Parsed records, one per line in the file.

    Raises
    ------
    IOError
        If the file cannot be opened or read.
    ValueError
        If parsing fails for all lines.
    """
    logger.info(f"Reading data file: {filename}")

    output_list: List[Dict[str, str]] = []

    required_columns = {
        "hgnc_id",
        "symbol",
        "name",
        "prev_symbol",
        "prev_name",
        "alias_symbol",
        "mane_select",
        "mane_plus_clinical",
    }

    try:
        with open(filename) as f:
            reader = csv.DictReader(f, delimiter="\t")

            if reader.fieldnames is None:
                raise ValueError("The .tsv file is empty or has no header line")

            logger.debug(f"Dataset contains {len(reader.fieldnames)} columns")
            print(reader.fieldnames)

            available_columns = []
            for column in required_columns:
                if column in reader.fieldnames:
                    available_columns.append(column)
                else:
                    logger.warning(f"Column {column} not available in dataset")

            if not available_columns:
                raise ValueError("No HGNC columns found for this gene")

            for row in reader:
                if None in row or any(value is None for value in row.values()):
                    continue

                print(row)
                lightweight_row = {}
                for column in available_columns:
                    if column in row:
                        lightweight_row[column] = row[column]

                output_list.append(lightweight_row)

        if not output_list:
            raise ValueError("No valid data parsed from file")

        logger.info(f"Successfully loaded {len(output_list)} records")
        return output_list

    except Exception:
        logger.exception("Error reading input file")
        raise

if __name__ == '__main__':
    setup_logging()
    logger.debug(f"Entry function")

    dataset = Path("/Users/diana/PycharmProjects/HGNC-Gene-Information-Web-Application/data/hgnc_test_set.txt")

    lightweight_dataset = read_file(dataset)

    output_path = dataset.parent / "lightweight_dataset.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(
            lightweight_dataset,
            file,
            indent=2,
            ensure_ascii=False,
        )
    sys.exit(0)