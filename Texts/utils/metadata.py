import json
import re
from pathlib import Path
from typing import Dict, List

from . import GenParazAcc, GetParazAcc, Paratranz


def Key(*args) -> str:
    idx = args[0]
    return f"MetaData-{idx}"


def File(*args) -> Path:
    name = args[0]
    file = Path(f"{name}.json")
    return file


WHITELIST = [
    re.compile("Exit the application", re.IGNORECASE),
]

IDX_LOWER_BOUND = 200
IDX_UPPER_BOUND = 10160


def ToParaTranz_name(in_root: Path) -> Dict[Path, List[Paratranz]]:
    file = in_root / "metadata" / "global-metadata-name.json"

    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

    ret = {}
    tmp = []

    for idx, item in enumerate(data):
        tmp.append(Paratranz(
            key=f"MetaData-name-{idx}-{item}",
            original=item,
            context=json.dumps({
                "Name": item,
                "Attr": "spellSchool",
                "Order": idx,
            }, ensure_ascii=False, indent=2),
        ))

    file = File("global-metadata-name")
    assert file not in ret
    ret[file] = tmp
    return ret


def ToParaTranz(in_root: Path) -> Dict[Path, List[Paratranz]]:
    ret = ToParaTranz_name(in_root)

    file = in_root / "metadata" / "global-metadata.json"

    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

    tmp = []

    for idx, item in enumerate(data):
        # Key, do not translate
        index = int(item["index"])
        value: str = item["value"]

        if index < IDX_LOWER_BOUND or index > IDX_UPPER_BOUND: continue

        if "\\n" in value:
            print(f"Ignore: {index}: {value}")
            continue

        # Found = False
        # for pat in WHITELIST:
        #     if pat.findall(value):
        #         Found = True
        #         break
        # if not Found:
        #     continue

        def adder(tag, key=None, data=item, name=index, idx=idx):
            nonlocal tmp
            tmp.append(Paratranz(
                key=Key(name),
                original=data[tag],
                context=json.dumps({}, ensure_ascii=False, indent=2),
            ))

        adder("value")

    file = File("global-metadata")
    assert file not in ret
    ret[file] = tmp

    return ret

def ToRaw_name(raw_root: Path, paraz_root: Path) -> Dict[Path, Dict]:
    file = raw_root / "metadata" / "global-metadata-name.json"

    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

    paraz_file = paraz_root / File("global-metadata-name")
    paraz_acc = GetParazAcc(paraz_file)

    ret = {}

    tmp = {}
    for idx, item in enumerate(data):
        def getter(tag, key=None, data=data, name=item, idx=idx):
            key=f"MetaData-name-{idx}-{item}"
            assert key in paraz_acc, key
            paraz_data = paraz_acc[key]
            assert data[tag] == paraz_data.original, \
                f"Mismatch:\n{data[tag]}\n{paraz_data.original}\nFile: global-metadata.json\nTranz: {paraz_file}"
            return paraz_data.translation

        assert item not in tmp
        tmp[item] = getter(idx)

    file = Path(".") / "global-metadata.name.json"
    ret[file] = tmp

    return ret


def ToRaw(raw_root: Path, paraz_root: Path) -> Dict[Path, Dict]:
    ret = ToRaw_name(raw_root, paraz_root)

    file = raw_root / "metadata" / "global-metadata.json"

    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

    paraz_file = paraz_root / File("global-metadata")
    paraz_acc = GetParazAcc(paraz_file)

    for idx, item in enumerate(data):
        # Key, do not translate
        index = int(item["index"])
        value: str = item["value"]

        if index < IDX_LOWER_BOUND or index > IDX_UPPER_BOUND: continue

        if "\\n" in value:
            print(f"Ignore: {index}: {value}")
            continue

        # Found = False
        # for pat in WHITELIST:
        #     if pat.findall(value):
        #         Found = True
        #         break
        # if not Found:
        #     continue

        def getter(tag, key=None, data=item, name=index, idx=idx):
            key = key if key else Key(name)
            assert key in paraz_acc, key
            paraz_data = paraz_acc[key]
            assert data[tag] == paraz_data.original, \
                f"Mismatch:\n{data[tag]}\n{paraz_data.original}\nFile: global-metadata.json\nTranz: {paraz_file}"
            return paraz_data.translation

        item["value"] = getter("value")

    file = Path(".") / "global-metadata.patch.json"
    ret[file] = data

    return ret
