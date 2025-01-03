import json
import shlex
from pathlib import Path
from typing import Dict, List

from . import GetParazAcc, Paratranz, kquote
from . import yarn_spinner_pb2 as pb


def Key(*args) -> str:
    case_name = args[0]
    node_name = args[1]
    inst_idx = args[2]
    idx = args[3]
    return f"{case_name}-{node_name}-{inst_idx}-{idx}"

def File(*args) -> Path:
    case_name = args[0]
    return Path(case_name).with_suffix(".json")

def extractor(op: List[str], pos: List[int]):
    ret = []
    for idx in pos:
        ret.append(op[idx])
    return ret

def importer(op: List[str], pos: List[int], texts: List[str]):
    for idx_text, idx_op in enumerate(pos):
        op[idx_op] = texts[idx_text]
    return

commands = {
    # "Heh… I usually only sell this stuff for 5sp a flask."
    "InterpretPrompt": [1, ],

    # "Commander White is stubborn and stuck in his ways. He seems to have a grudge against Ruby Tymora and will react negatively if you try to defend her. However, he will respect you if you defend yourself against personal attacks."
    "LoadArgueProfile": [1, ],

    # [
    #   "Assets/Visuals/Resources/Tutorials/Argument Tutorial.png",
    #   "Arguments",
    #   "You’ve started an ARGUMENT with another character. During an ARGUMENT, your opponent will make CLAIMS that you need to respond to. Responding correctly will lower your opponent’s CONFIDENCE. Responding incorrectly will lower [i]your[/i] CONFIDENCE. And once you run out of CONFIDENCE, you will lose the ARGUMENT."
    # ],
    "Tutorial": [2, 3],

    # "How did the bottle shatter?"
    "Deduction": [1, ],

    # "You lost the argument..."
    "Confirmation": [1, ],

    # "Episode End"
    "TitleCard": [1, ],

    # "It was selfish of me to learn magic."
    "Typewriter": [1, ],

    # "How did the bottle shatter?"
    "DeduceTypewriter": [1, ],

    # [0, "Celeste,The killer,Flinhart"]
    "SetDeductionField": [2, ],
}

def ToParaTranz(in_root: Path) -> Dict[Path, List[Paratranz]]:
    proto_bin_path = in_root / "case"

    ret = {}
    for proto_json in proto_bin_path.glob("Case *.json"):

        case_name = proto_json.name

        with open(proto_json, "r", encoding="utf8") as f:
            data = json.load(f)
            proto_bin = data["compiledYarnProgram"]["Array"]

        tmp: List[Paratranz] = []

        program = pb.Program() #type: ignore[attr-defined]
        program.ParseFromString(proto_bin)

        for node_name, node in program.nodes.items():
            for inst_idx, inst in enumerate(node.instructions):
                if inst.opcode != pb.Instruction.RUN_COMMAND:  #type: ignore[attr-defined]
                    continue

                for op in inst.operands:
                    if op.HasField("string_value"):
                        cmd = shlex.split(op.string_value)
                        if cmd[0] not in commands:
                            continue

                        strings = extractor(cmd, commands[cmd[0]])

                        for idx, ss in enumerate(strings):
                            tmp.append(Paratranz(
                                key=Key(case_name, node_name, inst_idx, idx),
                                original=ss,
                                context=json.dumps({
                                    "case": case_name,
                                    "node_name": node_name,
                                    "inst": str(inst),
                                    "op": str(op),
                                    "cmd": cmd,
                                }, ensure_ascii=False),
                            ))

        file = File(case_name)
        assert file not in ret
        ret[file] = tmp

    return ret


def ToRaw(raw_root: Path, paraz_root: Path) -> Dict[Path, Dict]:
    proto_bin_path = raw_root / "case"

    ret = {}

    for proto_json in proto_bin_path.glob("Case *.json"):

        case_name = proto_json.name

        with open(proto_json, "r", encoding="utf8") as f:
            data = json.load(f)
            proto_bin_json_data = data["compiledYarnProgram"]["Array"]
            proto_bin = bytearray(proto_bin_json_data)

        tmp: List[Paratranz] = []

        program = pb.Program() #type: ignore[attr-defined]
        program.ParseFromString(proto_bin)

        # Read corresponding Paratranz file
        paraz_file = paraz_root / File(case_name)
        paraz_acc = GetParazAcc(paraz_file)

        for node_name, node in program.nodes.items():
            for inst_idx, inst in enumerate(node.instructions):
                if inst.opcode != pb.Instruction.RUN_COMMAND:  #type: ignore[attr-defined]
                    continue

                for op in inst.operands:
                    if op.HasField("string_value"):
                        cmd = shlex.split(op.string_value)
                        if cmd[0] not in commands:
                            continue

                        strings = extractor(cmd, commands[cmd[0]])

                        texts_to_import = []
                        for idx, ss in enumerate(strings):
                            def getter(tag, key=None, data=strings, name=case_name, idx=idx):
                                key = key if key else Key(case_name, node_name, inst_idx, idx)
                                assert key in paraz_acc, key
                                paraz_data = paraz_acc[key]
                                assert data[tag] == paraz_data.original, \
                                    f"Mismatch:\n{data[tag]}\n{paraz_data.original}\nFile: {case_name}\nTranz: {paraz_file}"
                                # TODO(kuriko): add checker here
                                return paraz_data.translation

                            texts_to_import.append(getter(idx))

                        importer(cmd, commands[cmd[0]], texts=texts_to_import)
                        new_cmd = " ".join([kquote(s, idx) for idx, s in enumerate(cmd)])

                        print("="*80)
                        print(op.string_value)
                        print(new_cmd)

                        op.string_value = new_cmd

        new_proto_bin = program.SerializeToString()
        data["compiledYarnProgram"]["Array"] = list(new_proto_bin)

        file = Path("level0") / case_name
        ret[file] = data

    return ret
