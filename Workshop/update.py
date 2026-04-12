#!/usr/bin/env python3
"""Merge previous translations into freshly exported Paratranz JSON files.

Input:
- New export: paraz/1.game_gen_csv
- Previous translations: paraz/0.src/game_csv (can be missing or empty)

Output:
- Merged result: paraz/2.game_merge_csv
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List, Tuple


def load_json_list(path: Path) -> List[dict]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        return [x for x in data if isinstance(x, dict)]
    return []


def merge_file(new_items: List[dict], old_items: List[dict]) -> Tuple[List[dict], int]:
    old_by_key: Dict[str, dict] = {}
    for item in old_items:
        key = item.get("key")
        if isinstance(key, str) and key:
            old_by_key[key] = item

    reused = 0
    merged: List[dict] = []

    for new_item in new_items:
        out_item = dict(new_item)
        key = new_item.get("key")
        if isinstance(key, str) and key:
            old_item = old_by_key.get(key)
            if old_item and old_item.get("original") == new_item.get("original"):
                old_translation = old_item.get("translation")
                if isinstance(old_translation, str) and old_translation:
                    out_item["translation"] = old_translation
                    reused += 1
        merged.append(out_item)

    return merged, reused


def count_new_entries(new_items: List[dict], old_items: List[dict]) -> int:
    old_keys = {
        item.get("key")
        for item in old_items
        if isinstance(item.get("key"), str) and item.get("key")
    }
    count = 0
    for item in new_items:
        key = item.get("key")
        if isinstance(key, str) and key and key not in old_keys:
            count += 1
    return count


def main() -> int:
    parser = argparse.ArgumentParser(description="Merge old Paratranz translations into new export")
    parser.add_argument(
        "--old-dir",
        default="paraz/0.src/game_csv",
        help="Directory containing old JSON files (default: paraz/0.src/game_csv)",
    )
    parser.add_argument(
        "--new-dir",
        default="paraz/1.game_gen_csv",
        help="Directory containing newly exported JSON files (default: paraz/1.game_gen_csv)",
    )
    parser.add_argument(
        "--out-dir",
        default="paraz/2.game_merge_csv",
        help="Output directory for merged JSON files (default: paraz/2.game_merge_csv)",
    )
    args = parser.parse_args()

    new_dir = Path(args.new_dir)
    old_dir = Path(args.old_dir)
    out_dir = Path(args.out_dir)

    if not new_dir.exists() or not new_dir.is_dir():
        print(f"Error: new export directory not found: {new_dir}")
        return 1

    out_dir.mkdir(parents=True, exist_ok=True)

    new_files = sorted(new_dir.glob("*.json"))
    if not new_files:
        print(f"Error: no JSON files found in {new_dir}")
        return 1

    old_dir_exists = old_dir.exists() and old_dir.is_dir()

    total_files = 0
    total_items = 0
    total_reused = 0
    total_new_entries = 0
    files_with_new_entries: List[Tuple[str, int]] = []

    print(f"Merging {len(new_files)} files from {new_dir} ...")
    if not old_dir_exists:
        print(f"Old translation directory not found, using empty source: {old_dir}")

    for new_file in new_files:
        old_file = old_dir / new_file.name
        out_file = out_dir / new_file.name

        new_items = load_json_list(new_file)
        old_items = load_json_list(old_file) if old_dir_exists and old_file.exists() else []

        merged_items, reused = merge_file(new_items, old_items)
        new_entries = count_new_entries(new_items, old_items)

        with out_file.open("w", encoding="utf-8") as f:
            json.dump(merged_items, f, ensure_ascii=False, indent=2)

        total_files += 1
        total_items += len(merged_items)
        total_reused += reused
        total_new_entries += new_entries
        if new_entries > 0:
            files_with_new_entries.append((new_file.name, new_entries))
        print(f"  - {new_file.name}: items={len(merged_items)}, reused_translation={reused}")

    reuse_rate = (total_reused / total_items * 100) if total_items else 0.0
    print("Merge completed.")
    print(f"Output directory: {out_dir}")
    print(f"Processed files: {total_files}")
    print(f"Total items: {total_items}")
    print(f"Reused translations: {total_reused} ({reuse_rate:.1f}%)")
    print(f"New entries vs old source: {total_new_entries}")
    if total_new_entries > 0:
        print("WARNING: New entries detected in latest game definitions. Consider uploading these new items to Paratranz.")
        for name, count in files_with_new_entries:
            print(f"  - {name}: new_entries={count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
