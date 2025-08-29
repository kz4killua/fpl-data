import csv
import difflib
import json
import lzma
from pathlib import Path

DATA_DIR = Path("data")


def read_csv(path: Path) -> list[dict]:
    """Read a CSV file and return a list of dictionaries."""
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


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


def append_csv(rows: list[tuple], path: Path):
    """Append a list of tuples to a CSV file."""
    if not rows:
        return

    if not path.parent.exists():
        path.parent.mkdir(parents=True)

    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for row in rows:
            writer.writerow(row)


def read_compressed_json(path: Path) -> list[dict]:
    """Read a compressed JSON file."""
    with lzma.open(path, "rt", encoding="utf-8") as f:
        data = json.load(f)
    return data


def write_compressed_json(rows: list[dict], path: Path):
    """Write a list of dictionaries to a compressed JSON file."""
    if not rows:
        return

    if not path.parent.exists():
        path.parent.mkdir(parents=True)

    with lzma.open(path, "wt", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=4)


def map_closest_names(a: dict, b: dict):
    """Maps each name in a.values() with the most similar name in b.values()"""
    mappings = dict()

    # Get all possible key pairs, ranked by similarity
    pairs = [(k1, k2) for k1 in a for k2 in b]
    pairs.sort(
        key=lambda pair: calculate_similarity(a[pair[0]], b[pair[1]]), reverse=True
    )

    # Map each key in a to the closest key in b
    mapped_a = set()
    mapped_b = set()

    for pair in pairs:
        if not (pair[0] in mapped_a or pair[1] in mapped_b):
            mappings[pair[0]] = pair[1]
            mapped_a.add(pair[0])
            mapped_b.add(pair[1])

    return mappings


def calculate_similarity(s1: str, s2: str):
    """Returns a score indicating how similar two strings are."""
    s1 = s1.lower().strip()
    s2 = s2.lower().strip()
    matcher = difflib.SequenceMatcher(None, s1, s2)
    return matcher.ratio()
