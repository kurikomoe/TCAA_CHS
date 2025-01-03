import json
import logging
import re
from pathlib import Path
from typing import Dict, List

from pydantic import BaseModel, TypeAdapter

from . import flags

logger = logging.getLogger(__name__)

class Paratranz(BaseModel):
    key: str
    original: str
    translation: str|None = None
    context: str|None = None


def fix_slash_n(s: str) -> str:
    return s.replace("\\n", "\n")

def check_marks(a: str, b: str) -> bool:
    if not flags.ENABLE_MARK_CHECK: return True

    pat1 = re.compile(r"\[(\w+)/\]")
    pat2 = re.compile(r"\[(\w+)\].*?\[/\1\]")

    flag = True

    # stage 1
    ignored_controls = [ 'p', ]
    gp1 = pat1.findall(a)
    gp2 = pat1.findall(b)
    for ch in ignored_controls:
        while ch in gp1:
            gp1.remove(ch)
        while ch in gp2:
            gp2.remove(ch)
    flag = flag and gp1 == gp2

    # stage 2
    #! TODO(kuriko): modify this
    ignored_controls = [ 'i', 'b', ]

    gp1 = pat2.findall(a)
    gp2 = pat2.findall(b)
    for ch in ignored_controls:
        while ch in gp1:
            gp1.remove(ch)
        while ch in gp2:
            gp2.remove(ch)

    flag = flag and gp1 == gp2

    return flag

def GenParazAcc(data: List) -> Dict[str, Paratranz]:
    paraz_data = TypeAdapter(List[Paratranz]).validate_python(data)
    mm = {}
    for item in paraz_data:
        key = item.key

        item.original = fix_slash_n(item.original)

        if item.translation:
            item.translation = fix_slash_n(item.translation)
        else:
            item.translation = item.original

        if not check_marks(item.original, item.translation):
            logger.error("Mismatch marks")
            logger.error(item.original)
            logger.error(item.translation)
            input("cnt?")


        if item.context:
            item.context = fix_slash_n(item.context)

        assert key not in mm
        mm[key] = item

    return mm


def GetParazAcc(paraz_file: Path) -> Dict[str, Paratranz]:
    assert paraz_file.exists(), str(paraz_file)
    paraz_data = json.load(open(paraz_file, "r", encoding="utf-8"))
    paraz_acc = GenParazAcc(paraz_data)
    return paraz_acc


def kquote(s: str, idx) -> str:
    if idx == 0:
        return s
    elif s.isdigit():
        return s
    elif s.lower() in ["false", "true", "none"]:
        return s
    elif s == "":
        return '""'
    else:
        return f'"{s}"'
