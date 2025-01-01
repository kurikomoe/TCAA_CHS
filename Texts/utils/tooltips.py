import json
from pathlib import Path
from typing import Dict, List

from . import GetParazAcc, Paratranz


def Key(*args) -> str:
    name = args[0]
    return f"{name}"

def File(*args) -> Path:
    name = args[0]
    return Path(name)


def ToParaTranz(in_root: Path) -> Dict[Path, List[Paratranz]]:
    ret = {}

    tooltips_path = in_root / "tooltips"

    for tooltips_file in tooltips_path.glob("ShowTooltipOnMouseOver*.json"):
        with open(tooltips_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        tmp = []
        line = data['message']

        name = Path(tooltips_file).name

        tmp.append(Paratranz(
            key=Key(name),
            original=line,
            translation=None,
        ))

        file = File(name)
        assert file not in ret
        ret[file] = tmp

    return ret


def ToRaw(raw_root: Path, paraz_root: Path) -> Dict[Path, Dict]:
    ret = {}

    tooltips_path = raw_root / "tooltips"

    for tooltips_file in tooltips_path.glob("ShowTooltipOnMouseOver*.json"):
        with open(tooltips_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        name = Path(tooltips_file).name

        paraz_file = paraz_root / File(name)
        paraz_acc = GetParazAcc(paraz_file)

        def getter(tag, key=None, data=data, name=name, idx=0):
            key = key if key else Key(name, idx)
            assert key in paraz_acc
            paraz_data = paraz_acc[key]
            assert data[tag] == paraz_data.original, \
                f"Mismatch:\n{data[tag]}\n{paraz_data.original}\nFile: {name}\nTranz: {paraz_file}"
            return paraz_data.translation

        data['message'] = getter('message')

        file = Path("resources") / File(name)
        assert file not in ret
        ret[file] = data

    return ret
