import os
import json
from pathlib import Path
from typing import *
from . import Paratranz



def ToParaTranz(in_root: Path) -> Dict[str, List[Paratranz]]:
    ret = {}

    for file in in_root.glob("Default (en-US)*.json"):
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)

        lines = data['_stringTable']['values']['Array']

        name = Path(file).stem

        tmp = []
        for idx, line in enumerate(lines):
            tmp.append(Paratranz(
                key=f"{name}-{idx}",
                original=line,
                translation=None,
                context="遇到人名，例如「Kuriko: Speak English」请保留 「Kuriko: 」，遇到其他控制符也行保留，或者询问程序",
            ))
        ret[name] = tmp

    return ret
