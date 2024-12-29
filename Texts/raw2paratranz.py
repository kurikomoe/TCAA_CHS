import io
import json
from pathlib import Path
from pydantic.json import pydantic_encoder

import argparse

from utils import Paratranz


'''
[
  {
    "key": "KEY 键值",
    "original": "source text 原文",
    "translation": "translation text 译文",
    "context": "Context 上下文 (for info)"
  },
  {
    "key": "KEY 键值 2",
    "original": "source text 原文 2",
    "translation": "translation text 译文 2"
  }
]
'''
parser = argparse.ArgumentParser(description='Convert raw text to Paratranz JSON format')
parser.add_argument('--input', type=str, help='Input folder')
parser.add_argument('--output', type=str, help='Output folder')
parser.add_argument('--type', type=str, choices=["serifu", "m_text", "charalist"], help='Input Folder')

args = parser.parse_args()

in_root = Path(args.input)
out_root = Path(args.output) / args.type

out_root.mkdir(parents=True, exist_ok=True)

ret = None
if args.type == "serifu":
    # 台本 aka defaultxxx
    from utils.serifu import ToParaTranz
    ret = ToParaTranz(in_root)
elif args.type == "m_text":
    # mono behaviour text
    from utils.m_text import ToParaTranz
    ret = ToParaTranz(in_root)
elif args.type == "charalist":
    # aka CharacterLibrary-level0-599.json
    from utils.charalist import ToParaTranz
    ret = ToParaTranz(in_root)

assert ret is not None

for name, data in ret.items():
    data: Paratranz = data
    with open(out_root / f"{name}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=pydantic_encoder)
