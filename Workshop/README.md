# TCAA CSV <-> Paratranz Workflow Notes

## 目录约定

- 原始游戏 CSV：`game/orig`（只读访问，不可直接修改）
- 导出 JSON：`paraz/game_csv`
- 旧翻译来源（可为空）：`paraz/src/game_csv`
- 合并输出：`paraz/game_merge_csv`
- 回写后的可编辑 CSV（可选）：`game/output`

## 导入游戏前检查清单

在将翻译回写到可编辑 CSV 并导入游戏前，请先检查：

1. 所有翻译列必须是 `TRANSLATION` 或 `XXX TRANSLATION`（大小写不限）。
2. `XXX TRANSLATION` 必须能找到对应原文字段 `XXX`。
3. 避免表头拼写错误（例如 `EPISODE` 写成 `EPSIODE` 会导致映射失败）。
4. 导出后可抽查 `paraz/game_csv/*.json`，确认 `original` 与 `context` 正确。
5. 合并后抽查 `paraz/game_merge_csv/*.json`，确认旧翻译复用正确。
6. 不要直接改 `game/orig`，回写输出请使用 `game/output`。

## 常用命令

```bash
python3 to_paraz.py --game-dir game/orig --out-dir paraz/game_csv
python3 update.py --new-dir paraz/game_csv --old-dir paraz/src/game_csv --out-dir paraz/game_merge_csv
python3 to_game_csv.py --source-game-dir game/orig --out-game-dir game/output --json-dir paraz/game_merge_csv
```

## Justfile 流程

```bash
just export
just merge
just all
```

## 说明

- 当前 key 方案：`<csv_name>::<translation_column>::<sha1(original)[:16]>`
- 该方案不依赖行号，便于在原文未改动时复用翻译。
