import argparse
import json
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", type=str, help="something like Case 1-sharedassets0.assets-154.json")

args = parser.parse_args()

stem = Path(args.input)

with open(args.input) as f:
    data = json.load(f)
    data = data["compiledYarnProgram"]["Array"]
    data = bytearray(data)

with open(f"{stem}.bin", "wb") as f:
    f.write(data)
