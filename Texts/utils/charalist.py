import json
from pathlib import Path
from typing import Dict, List

from . import GetParazAcc, Paratranz

IGNORED_OCCUPATION = [ "???", ]
IGNORED_ARCANE_ART = [ "None", ]

def Key(*args) -> str:
    name = args[0]
    tag = args[1]
    return f"{name}-{tag}"

def Key2(*args) -> str:
    name = args[0]
    idx = args[1]
    return f"{name}-altDescriptions-{idx}"

def File(*args) -> Path:
    name = args[0]
    return Path(f"{name}.json")

def ToParaTranz(in_root: Path) -> Dict[Path, List[Paratranz]]:
    ret = {}

    charalist_file = in_root / "CharacterLibrary-level0-599.json"
    with open(charalist_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    for chara in data["characterList"]["Array"]:
        tmp = []

        name = chara["name"]

        def adder(tag, key=None):
            nonlocal tmp, name, chara
            tmp.append(Paratranz(
                key=Key(name, tag),
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

        for idx, alt in enumerate(chara["altDescriptions"]["Array"]):
            tmp.append(Paratranz(
                key=Key2(name, idx),
                original=alt,
                context=json.dumps({
                    "Name": name,
                    "Attr": "altDescriptions",
                    "idx": idx,
                }, ensure_ascii=False),
            ))

        occupation = chara["occupation"]
        if occupation not in IGNORED_OCCUPATION:
            adder("occupation")

        arcane_art = chara["arcaneArt"]
        if arcane_art not in IGNORED_ARCANE_ART:
            adder("arcaneArt")

        file = File(name)
        assert file not in ret
        ret[file] = tmp

    return ret


def ToRaw(raw_root: Path, paraz_root: Path) -> Dict[Path, Dict]:
    base_file = Path("CharacterLibrary-level0-599.json")

    raw_file = raw_root / base_file

    with open(raw_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    ret: Dict[Path, Dict] = {}

    for idx, chara in enumerate(data["characterList"]["Array"]):
        # Key, do not translate
        name = chara["name"]

        # Read corresponding Paratranz file
        paraz_file = paraz_root / File(name)
        paraz_acc = GetParazAcc(paraz_file)

        def getter(tag, key=None, data=chara, name=name, idx=idx):
            key = key if key else Key(name, tag)
            assert key in paraz_acc, key
            paraz_data = paraz_acc[key]
            assert data[tag] == paraz_data.original, \
                f"Mismatch:\n{data[tag]}\n{paraz_data.original}\nFile: {base_file}\nTranz: {paraz_file}"
            # TODO(kuriko): add checker here
            return paraz_data.translation

        chara["displayName"] = getter("displayName")

        chara["description"] = getter("description")

        for idx, _ in enumerate(chara["altDescriptions"]["Array"]):
            chara["altDescriptions"]["Array"][idx] = getter(idx, data=chara["altDescriptions"]["Array"], key=Key2(name, idx))

        if chara["occupation"] not in IGNORED_OCCUPATION:
            chara["occupation"] = getter("occupation")

        if chara["arcaneArt"] not in IGNORED_ARCANE_ART:
            chara["arcaneArt"] = getter("arcaneArt")

    file = "level0" / base_file
    ret[file] = data

    return ret
