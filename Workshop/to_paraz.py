#!/usr/bin/env python3
"""Export game CSV files to Paratranz JSON format.

Output item format:
{
  "key": "...",
  "original": "...",
  "translation": "...",
  "context": "{...pretty json...}"
}

Key format:
<csv_name>::<translation_column>::<sha1(original)[:16]>
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


def normalize_context_key(col: str) -> str:
    return col.strip().lower()


def find_source_column(headers: List[str], trans_col: str) -> str | None:
    t = trans_col.strip()
    up = t.upper()

    # Generic single translation column.
    if up == "TRANSLATION":
        if "text" in headers:
            return "text"
        if "TEXT" in headers:
            return "TEXT"
        return None

    # Named translation column: "X TRANSLATION" -> source "X" if exists.
    if up.endswith(" TRANSLATION"):
        base = t[: -len(" TRANSLATION")].strip()

        # Exact match first.
        if base in headers:
            return base

        # Fallback for abbreviated columns like HEADER TRANSLATION -> TUTORIAL HEADER.
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


def row_to_context(headers: List[str], row: Dict[str, str]) -> Dict[str, str]:
    ctx: Dict[str, str] = {}
    for h in headers:
        if not h:
            continue
        if is_translation_column(h):
            continue
        ctx[normalize_context_key(h)] = row.get(h, "")
    return ctx


def make_original_hash(original: str) -> str:
    return hashlib.sha1(original.encode("utf-8")).hexdigest()[:16]


def make_key(csv_name: str, trans_col: str, original: str) -> str:
    # Stable key for reuse when row order/count changes.
    return f"{csv_name}::{trans_col}::{make_original_hash(original)}"


def export_one_csv(csv_path: Path, out_dir: Path) -> Tuple[int, int]:
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        print(csv_path);
        raw_headers = reader.fieldnames or []
        headers = [h for h in raw_headers if h is not None]

        trans_pairs: List[Tuple[str, str]] = []
        for h in headers:
            if not h or not is_translation_column(h):
                continue
            src = find_source_column(headers, h)
            if src:
                trans_pairs.append((h, src))

        item_map: Dict[str, Dict[str, str]] = {}
        row_count = 0
        for row_count, row in enumerate(reader, start=1):
            ctx_obj = row_to_context(headers, row)
            ctx_str = json.dumps(ctx_obj, ensure_ascii=False, indent=2)

            for trans_col, src_col in trans_pairs:
                original_raw = row.get(src_col, "") or ""
                if not original_raw.strip():
                    continue
                translation = (row.get(trans_col, "") or "")
                key = make_key(csv_path.name, trans_col, original_raw)
                existing = item_map.get(key)
                if existing is None:
                    item_map[key] = {
                        "key": key,
                        "original": original_raw,
                        "translation": translation,
                        "context": ctx_str,
                    }
                elif not existing.get("translation") and translation:
                    existing["translation"] = translation

        items = list(item_map.values())

    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{csv_path.stem}.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

    return row_count, len(items)


def main() -> int:
    parser = argparse.ArgumentParser(description="Export game CSV files to Paratranz JSON")
    parser.add_argument(
        "--game-dir",
        default="game/orig",
        help="Directory containing source CSV files (default: game/orig)",
    )
    parser.add_argument(
        "--out-dir",
        default="paraz/1.game_gen_csv",
        help="Output directory for per-CSV JSON files (default: paraz/1.game_gen_csv)",
    )
    args = parser.parse_args()

    game_dir = Path(args.game_dir)
    out_dir = Path(args.out_dir)

    if not game_dir.exists() or not game_dir.is_dir():
        print(f"Error: game directory not found: {game_dir}")
        return 1

    csv_files = sorted(game_dir.glob("*.csv"))
    if not csv_files:
        print(f"Error: no CSV files found in {game_dir}")
        return 1

    total_rows = 0
    total_items = 0
    print(f"Exporting {len(csv_files)} CSV files from {game_dir} ...")

    for csv_file in csv_files:
        rows, items = export_one_csv(csv_file, out_dir)
        total_rows += rows
        total_items += items
        print(f"  - {csv_file.name}: {items} items ({rows} rows)")

    print("Export completed.")
    print(f"Output directory: {out_dir}")
    print(f"Total rows scanned: {total_rows}")
    print(f"Total Paratranz items: {total_items}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
