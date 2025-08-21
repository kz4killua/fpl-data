import csv
import json
import lzma
from pathlib import Path

DATA_DIR = Path("data")


def write_csv(rows: list[dict], path: Path):
    """Write a list of dictionaries to a CSV file."""
    if not rows:
        return

    if not path.parent.exists():
        path.parent.mkdir(parents=True)

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


def append_csv(rows: list, path: Path):
    """Append a list of rows to a CSV file."""
    if not rows:
        return

    if not path.parent.exists():
        path.parent.mkdir(parents=True)

    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for row in rows:
            writer.writerow(row)


def write_json_xz(rows: list[dict], path: Path):
    """Write a list of dictionaries to a compressed JSON file."""
    if not rows:
        return

    if not path.parent.exists():
        path.parent.mkdir(parents=True)

    with lzma.open(path, "wt", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=4)
