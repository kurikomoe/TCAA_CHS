#!/usr/bin/env python3
"""Import Paratranz JSON translations into writable CSV copies.

Expected JSON item format:
{
  "key": "<csv_name>::<translation_column>::<sha1(original)[:16]>",
  "original": "...",
  "translation": "...",
  "context": "{...}"
}
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Dict, List, Tuple


def is_translation_column(col: str) -> bool:
    c = col.strip()
    if not c:
        return False
    up = c.upper()
    return up == "TRANSLATION" or up.endswith(" TRANSLATION")


def find_source_column(headers: List[str], trans_col: str) -> str | None:
    t = trans_col.strip()
    up = t.upper()

    if up == "TRANSLATION":
        if "text" in headers:
            return "text"
        if "TEXT" in headers:
            return "TEXT"
        return None

    if up.endswith(" TRANSLATION"):
        base = t[: -len(" TRANSLATION")].strip()
        if base in headers:
            return base

        base_up = base.upper()
        candidates = [
            h
            for h in headers
            if h
            and not is_translation_column(h)
            and h.upper().endswith(" " + base_up)
        ]
        if len(candidates) == 1:
            return candidates[0]
    return None


def make_original_hash(original: str) -> str:
    return hashlib.sha1(original.encode("utf-8")).hexdigest()[:16]


def parse_new_key(key: str) -> Tuple[str, str, str] | None:
    parts = key.split("::", 2)
    if len(parts) != 3:
        return None
    csv_name, trans_col, original_hash = parts
    if not csv_name or not trans_col or not original_hash:
        return None
    return csv_name, trans_col, original_hash


def load_updates(json_dir: Path) -> Dict[str, Dict[str, Dict[str, str]]]:
    # csv_name -> trans_col -> original_text -> translation
    text_updates: Dict[str, Dict[str, Dict[str, str]]] = {}

    for json_file in sorted(json_dir.glob("*.json")):
        with json_file.open("r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            continue

        for item in data:
            if not isinstance(item, dict):
                continue
            key = item.get("key", "")
            translation = item.get("translation", "")
            if translation is None:
                translation = ""

            new_parsed = parse_new_key(key)
            if new_parsed:
                csv_name, trans_col, expected_hash = new_parsed
                original = item.get("original", "")
                if original is None:
                    original = ""
                if make_original_hash(original) != expected_hash:
                    continue
                text_updates.setdefault(csv_name, {}).setdefault(trans_col, {})[
                    original
                ] = translation
    return text_updates


def apply_updates_to_csv(
    source_csv_path: Path,
    output_csv_path: Path,
    file_text_updates: Dict[str, Dict[str, str]],
) -> Tuple[int, int]:
    with source_csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        rows: List[Dict[str, str]] = list(reader)

    changed_cells = 0
    changed_rows = 0

    # Apply updates by matching source text, not row number.
    trans_to_source: Dict[str, str] = {}
    for trans_col in file_text_updates.keys():
        src_col = find_source_column(list(headers), trans_col)
        if src_col:
            trans_to_source[trans_col] = src_col

    for row in rows:
        row_changed = False
        for trans_col, source_map in file_text_updates.items():
            if trans_col not in headers:
                continue
            src_col = trans_to_source.get(trans_col)
            if not src_col:
                continue

            original = row.get(src_col, "")
            if original is None:
                original = ""

            if original not in source_map:
                continue

            new_value = source_map[original]
            old_value = row.get(trans_col, "")
            if old_value is None:
                old_value = ""
            if new_value is None:
                new_value = ""

            if old_value != new_value:
                row[trans_col] = new_value
                changed_cells += 1
                row_changed = True

        if row_changed:
            changed_rows += 1

    output_csv_path.parent.mkdir(parents=True, exist_ok=True)
    with output_csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    return changed_rows, changed_cells


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Import Paratranz JSON translations into writable CSV copies"
    )
    parser.add_argument(
        "--source-game-dir",
        default="game/orig",
        help="Directory containing source CSV files (default: game/orig)",
    )
    parser.add_argument(
        "--out-game-dir",
        default="game/output",
        help="Directory to write translated CSV files (default: game/output)",
    )
    parser.add_argument(
        "--json-dir",
        default="paraz/2.game_merge_csv",
        help="Directory containing merged Paratranz JSON files (default: paraz/2.game_merge_csv)",
    )
    args = parser.parse_args()

    source_game_dir = Path(args.source_game_dir)
    out_game_dir = Path(args.out_game_dir)
    json_dir = Path(args.json_dir)

    if not source_game_dir.exists() or not source_game_dir.is_dir():
        print(f"Error: source game directory not found: {source_game_dir}")
        return 1
    if not json_dir.exists() or not json_dir.is_dir():
        print(f"Error: json directory not found: {json_dir}")
        return 1

    out_game_dir.mkdir(parents=True, exist_ok=True)

    text_updates = load_updates(json_dir)
    if not text_updates:
        print("No translation updates found.")
        return 0

    print(f"Applying updates from {json_dir} ...")

    total_changed_rows = 0
    total_changed_cells = 0
    processed_files = 0

    for csv_name in sorted(text_updates.keys()):
        source_csv_path = source_game_dir / csv_name
        output_csv_path = out_game_dir / csv_name
        if not source_csv_path.exists():
            print(f"  - skip missing CSV: {csv_name}")
            continue

        file_text_updates = text_updates.get(csv_name, {})

        changed_rows, changed_cells = apply_updates_to_csv(
            source_csv_path,
            output_csv_path,
            file_text_updates,
        )
        processed_files += 1
        total_changed_rows += changed_rows
        total_changed_cells += changed_cells
        print(
            f"  - {csv_name}: updated {changed_cells} cells in {changed_rows} rows"
        )

    print("Import completed.")
    print(f"Processed files: {processed_files}")
    print(f"Changed rows: {total_changed_rows}")
    print(f"Changed cells: {total_changed_cells}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
