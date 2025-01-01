import json
from pathlib import Path
from typing import Dict, List

from . import GetParazAcc, Paratranz


def Key(*args) -> str:
    name = args[0]
    idx = args[1]
    return f"{name}-{idx}"

def File(*args) -> Path:
    serifu_file_name = args[0]
    return Path(serifu_file_name)


def ToParaTranz(in_root: Path) -> Dict[Path, List[Paratranz]]:
    ret = {}

    serifu_path = in_root / "serifu"

    for serifu_file in serifu_path.glob("Default (en-US)*.json"):
        with open(serifu_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        lines = data['_stringTable']['values']['Array']

        name = Path(serifu_file).stem

        tmp = []
        for idx, line in enumerate(lines):
            tmp.append(Paratranz(
                key=f"{name}-{idx}",
                original=line,
                translation=None,
                context="遇到人名，例如「Kuriko: Speak English」请保留 「Kuriko: 」，遇到其他控制符也行保留，或者询问程序",
            ))

        file = File(serifu_file.name)
        assert file not in ret
        ret[file] = tmp

    return ret


def ToRaw(raw_root: Path, paraz_root: Path) -> Dict[Path, Dict]:
    serifu_path = raw_root / "serifu"

    ret = {}

    for serifu_file in serifu_path.glob("Default (en-US)*.json"):
        with open(serifu_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        lines = data['_stringTable']['values']['Array']

        name = Path(serifu_file).stem

        paraz_file = paraz_root / File(serifu_file.name)
        paraz_acc = GetParazAcc(paraz_file)

        for idx, _ in enumerate(lines):
            def getter(tag, key=None, data=lines, name=name, idx=idx):
                key = key if key else Key(name, idx)
                assert key in paraz_acc
                paraz_data = paraz_acc[key]
                assert data[tag] == paraz_data.original, \
                    f"Mismatch:\n{data[tag]}\n{paraz_data.original}\nFile: {serifu_file}\nTranz: {paraz_file}"
                # TODO(kuriko): add checker here
                return paraz_data.translation

            lines[idx] = getter(idx)

        file = Path("resources") / File(serifu_file.name)
        assert file not in ret
        ret[file] = data

    return ret
