import json
import shlex
from pathlib import Path
from typing import Dict, List

from . import Paratranz
from . import yarn_spinner_pb2 as pb


def extractor(op: List[str], pos: List[int]):
    ret = []
    for idx in pos:
        ret.append(op[idx])
    return ret

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
    for proto_bin in proto_bin_path.glob("Case *.bin"):
        with open(proto_bin, "rb") as f:
            data = f.read()

        case_name = proto_bin.stem

        tmp: List[Paratranz] = []

        program = pb.Program() #type: ignore[attr-defined]
        program.ParseFromString(data)

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
                                key=f"{case_name}-{node_name}-{inst_idx}-{idx}",
                                original=ss,
                                context=json.dumps({
                                    "case": case_name,
                                    "node_name": node_name,
                                    "inst": str(inst),
                                    "op": str(op),
                                    "cmd": cmd,
                                }, ensure_ascii=False),
                            ))

        file = Path(case_name).with_suffix(".json")
        assert file not in ret
        ret[file] = tmp

    return ret
