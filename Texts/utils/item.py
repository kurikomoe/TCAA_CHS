import json
from pathlib import Path
from typing import Dict, List

from pydantic.json import pydantic_encoder

from . import GenParazAcc, GetParazAcc, Paratranz


def Key(*args) -> str:
    item_container_name = args[0]
    idx = args[1]
    name = args[2]
    tag = args[3]
    return f"Item-{item_container_name}-{idx}-{name}-{tag}"

def File(*args) -> Path:
    item_container_name = args[0]
    idx = args[1]
    return Path(item_container_name) / f"{idx}.json"

def ToParaTranz(in_root: Path) -> Dict[Path, List[Paratranz]]:
    file = in_root / "ItemLibrary-level0-603.json"

    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

    ret = {}
    for _, item_container in enumerate(data['items']["Array"]):
        item_container_name = item_container["name"]

        if item_container_name == "Test": continue

        for idx, item in enumerate(item_container["itemList"]["Array"]):
            tmp = []

            # Key, do not translate
            name = item["name"]

            def adder(tag, key=None, data=item, name=name, idx=idx):
                nonlocal tmp
                tmp.append(Paratranz(
                    key=key if key else Key(item_container_name, idx, name, tag),
                    original=data[tag],
                    context=json.dumps({
                        "Name": name,
                        "Idx": idx,
                        "Attr": tag,
                    }, ensure_ascii=False),
                ))

            display_name = item["displayName"]
            adder("displayName")

            description = item["description"]
            adder("description")

            file = File(item_container_name, idx)
            assert file not in ret
            ret[file] = tmp

    return ret


def ToRaw(raw_root: Path, paraz_root: Path) -> Dict[Path, Dict]:
    base_file = Path("ItemLibrary-level0-603.json")

    raw_file = raw_root / base_file

    with open(raw_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    ret: Dict[Path, Dict] = {}

    for _, item_container in enumerate(data['items']["Array"]):
        item_container_name = item_container["name"]

        if item_container_name == "Test": continue

        for idx, item in enumerate(item_container["itemList"]["Array"]):
            # Key, do not translate
            name = item["name"]

            # Read corresponding Paratranz file
            paraz_file = paraz_root / File(item_container_name, idx)
            paraz_acc = GetParazAcc(paraz_file)

            def getter(tag, key=None, data=item, name=name, idx=idx):
                key = key if key else Key(item_container_name, idx, name, tag)
                assert key in paraz_acc
                paraz_data = paraz_acc[key]
                assert data[tag] == paraz_data.original, \
                    f"Mismatch:\n{data[tag]}\n{paraz_data.original}\nFile: {base_file}\nTranz: {paraz_file}"
                # TODO(kuriko): add checker here
                return paraz_data.translation

            item["displayName"] = getter("displayName")
            item["description"] = getter("description")

    file = "level0" / base_file
    ret[file] = data

    return ret
