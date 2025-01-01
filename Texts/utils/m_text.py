import json
from pathlib import Path
from typing import Dict, List

from . import GetParazAcc, Paratranz


def Key(*args) -> str:
    name = args[0]
    return f"{name}"

def File(*args) -> Path:
    pattern = args[0]
    return Path(f"{pattern}.json")

def ToParaTranz(in_root: Path) -> Dict[Path, List[Paratranz]]:
    ret = {}

    in_root = "m_text" / in_root

    for pattern in ["level0", "resources"]:
        tmp = []
        for file in in_root.glob(pattern + "/TextMeshProUGUI*.json"):
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)

            line = data['m_text']

            name = Path(file).stem

            tmp.append(Paratranz(
                key=Key(name),
                original=line,
                translation=None,
            ))

        file = File(pattern)
        assert file not in ret
        ret[file] = tmp

    return ret


def ToRaw(raw_root: Path, paraz_root: Path) -> Dict[Path, Dict]:
    ret = {}

    m_text_path = raw_root / "m_text"

    for pattern in ["level0", "resources"]:
        paraz_file = paraz_root / File(pattern)
        paraz_acc = GetParazAcc(paraz_file)

        for file in m_text_path.glob(pattern + "/TextMeshProUGUI*.json"):
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)

            name = Path(file).stem

            def getter(tag, key=None, data=data, name=name, idx=0):
                key = key if key else Key(name)
                assert key in paraz_acc, key
                paraz_data = paraz_acc[key]
                assert data[tag] == paraz_data.original, \
                    f"Mismatch:\n{data[tag]}\n{paraz_data.original}\nFile: {name}\nTranz: {paraz_file}"
                return paraz_data.translation

            data['m_text'] = getter('m_text')

            file = Path(pattern) / File(name)
            assert file not in ret
            ret[file] = data

    return ret
