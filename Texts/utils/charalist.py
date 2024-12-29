import os
import json
from pathlib import Path
from typing import *
from . import Paratranz



def ToParaTranz(in_root: Path) -> Dict[str, List[Paratranz]]:
    ret = {}

    charalist_file = in_root / "level0" / "CharacterLibrary-level0-599.json"
    with open(charalist_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    for chara in data["characterList"]["Array"]:
        tmp = []

        name = chara["name"]

        def adder(tag, key=None):
            nonlocal tmp, name
            tmp.append(Paratranz(
                key = key if key else f"{name}-{tag}",
                original=chara[tag],
                context=json.dumps({
                    "Name": name,
                    "Attr": tag,
                }, ensure_ascii=False),
            ))


        displayName = chara["displayName"]
        adder("displayName")

        description = chara["description"]
        adder("description")

        altDescriptions = []
        for idx, alt in enumerate(chara["altDescriptions"]["Array"]):
            tmp.append(Paratranz(
                key = f"{name}-{altDescriptions}-{idx}",
                original=alt,
                context=json.dumps({
                    "Name": name,
                    "Attr": altDescriptions,
                    "idx": idx
                }, ensure_ascii=False),
            ))

        occupation = chara["occupation"]
        if occupation not in ["???"]:
            adder("occupation")

        arcaneArt = chara["arcaneArt"]
        if arcaneArt not in ["None"]:
            adder("arcaneArt")

        assert name not in tmp
        ret[name] = tmp

    return ret
