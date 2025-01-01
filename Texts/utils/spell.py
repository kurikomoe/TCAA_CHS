import json
from pathlib import Path
from typing import Dict, List

from . import GenParazAcc, GetParazAcc, Paratranz


def Key(*args) -> str:
    idx = args[0]
    name = args[1]
    tag = args[2]
    return f"SpellLibrary-{idx}-{name}-{tag}"


def File(*args) -> Path:
    name = args[0]
    file = Path(f"{name}.json")
    return file


def ToParaTranz(in_root: Path) -> Dict[Path, List[Paratranz]]:
    file = in_root / "SpellLibrary-level0-602.json"

    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

    ret = {}
    for idx, spell in enumerate(data['spellList']["Array"]):
        tmp = []

        # Key, do not translate
        name = spell["name"]

        def adder(tag, key=None, data=spell, name=name, idx=idx):
            nonlocal tmp
            tmp.append(Paratranz(
                key=key if key else Key(idx, name, tag),
                original=data[tag],
                context=json.dumps({
                    "Name": name,
                    "Idx": idx,
                    "Attr": tag,
                }, ensure_ascii=False),
            ))

        display_name = spell["displayName"]
        adder("displayName")

        description = spell["description"]
        adder("description")

        incantation = spell["incantation"]
        adder("incantation")

        gesture = spell["gesture"]
        adder("gesture")

        duration = spell["duration"]
        adder("duration")

        file = File(name)
        assert file not in ret
        ret[file] = tmp

    return ret


def ToRaw(raw_root: Path, paraz_root: Path) -> Dict[Path, Dict]:
    base_file = Path("SpellLibrary-level0-602.json")

    raw_file = raw_root / base_file

    with open(raw_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    ret: Dict[Path, Dict] = {}

    for idx, spell in enumerate(data['spellList']["Array"]):
        # Key, do not translate
        name = spell["name"]

        # Read corresponding Paratranz file
        paraz_file = paraz_root / File(name)
        paraz_acc = GetParazAcc(paraz_file)

        def getter(tag, key=None, data=spell, name=name, idx=idx):
            key = key if key else Key(idx, name, tag)
            assert key in paraz_acc
            paraz_data = paraz_acc[key]
            assert data[tag] == paraz_data.original, \
                f"Mismatch:\n{data[tag]}\n{paraz_data.original}\nFile: {base_file}\nTranz: {paraz_file}"
            # TODO(kuriko): add checker here
            return paraz_data.translation

        spell["displayName"] = getter("displayName")

        spell["description"] = getter("description")

        spell["incantation"] = getter("incantation")

        spell["gesture"] = getter("gesture")

        spell["duration"] = getter("duration")

    file = "level0" / base_file
    ret[file] = data

    return ret
