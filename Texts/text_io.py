import argparse
import json
from pathlib import Path

from pydantic.json import pydantic_encoder
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
parser = argparse.ArgumentParser(
    description='Convert raw text to Paratranz JSON format')
parser.add_argument('--export', dest="export_flag",
                    action="store_true", help='export mode')
parser.add_argument('--import', dest="import_flag",
                    action="store_true", help='import mode')

parser.add_argument('--type', type=str, choices=[
    "serifu",
    "m_text",
    "charalist",
    "case",
    "spell",
    "item",
    "tooltips",
], help='Input Folder')

parser.add_argument('--raw', type=str, help='@old')
parser.add_argument('--paraz', type=str, help='@paraz')

# only in import mode
parser.add_argument('--out', type=str, help='@new')

args = parser.parse_args()


def export_mode():
    raw_root = Path(args.raw)
    paraz_root = Path(args.paraz) / args.type

    in_root = raw_root
    out_root = paraz_root
    out_root.mkdir(parents=True, exist_ok=True)

    ret = None
    if args.type == "serifu":  # 台本 aka defaultxxx
        from utils.serifu import ToParaTranz
        ret = ToParaTranz(in_root)
    elif args.type == "m_text":  # mono behaviour text
        from utils.m_text import ToParaTranz
        ret = ToParaTranz(in_root)
    elif args.type == "charalist":  # aka CharacterLibrary-level0-599.json
        from utils.charalist import ToParaTranz
        ret = ToParaTranz(in_root)
    elif args.type == "spell":  # protobuf dumps
        from utils.spell import ToParaTranz
        ret = ToParaTranz(in_root)
    elif args.type == "item":  # protobuf dumps
        from utils.item import ToParaTranz
        ret = ToParaTranz(in_root)
    elif args.type == "case":  # protobuf dumps
        from utils.case import ToParaTranz
        ret = ToParaTranz(in_root)
    elif args.type == "tooltips":  # protobuf dumps
        from utils.tooltips import ToParaTranz
        ret = ToParaTranz(in_root)

    assert ret is not None

    for file, data in ret.items():
        out_file = out_root / file
        out_file.parent.mkdir(parents=True, exist_ok=True)
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2, default=pydantic_encoder)


def import_mode():
    raw_root = Path(args.raw)
    paraz_root = Path(args.paraz) / args.type
    out_root = Path(args.out)

    ret = None
    if args.type == "serifu":  # 台本 aka defaultxxx
        from utils.serifu import ToRaw
        ret = ToRaw(raw_root, paraz_root)
    elif args.type == "m_text":  # mono behaviour text
        from utils.m_text import ToRaw
        ret = ToRaw(raw_root, paraz_root)
    elif args.type == "charalist":  # aka CharacterLibrary-level0-599.json
        from utils.charalist import ToRaw
        ret = ToRaw(raw_root, paraz_root)
    elif args.type == "spell":  # protobuf dumps
        from utils.spell import ToRaw
        ret = ToRaw(raw_root, paraz_root)
    elif args.type == "item":  # protobuf dumps
        from utils.item import ToRaw
        ret = ToRaw(raw_root, paraz_root)
    elif args.type == "case":  # protobuf dumps
        from utils.case import ToRaw
        ret = ToRaw(raw_root, paraz_root)
    elif args.type == "tooltips":  # protobuf dumps
        from utils.tooltips import ToRaw
        ret = ToRaw(raw_root, paraz_root)

    assert ret is not None

    for file, data in ret.items():
        out_file = out_root / file
        out_file.parent.mkdir(parents=True, exist_ok=True)
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2, default=pydantic_encoder)


if args.export_flag:
    export_mode()
elif args.import_flag:
    import_mode()
