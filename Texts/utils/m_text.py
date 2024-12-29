import os
import json
from pathlib import Path
from typing import *
from . import Paratranz



def ToParaTranz(in_root: Path) -> Dict[str, List[Paratranz]]:
    ret = {}

    for pattern in ["level0", "resources"]:
        tmp = []
        for file in in_root.glob(pattern + "/TextMeshProUGUI*.json"):
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)

            line = data['m_text']

            name = Path(file).stem

            tmp.append(Paratranz(
                key=f"{name}",
                original=line,
                translation=None,
            ))

        ret[pattern] = tmp

    return ret
