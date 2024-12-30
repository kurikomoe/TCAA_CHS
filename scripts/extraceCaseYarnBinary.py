import json

with open("Case 1-sharedassets0.assets-154.json") as f:
    data = json.load(f)
    data = data["compiledYarnProgram"]["Array"]
    data = bytearray(data)

with open("yarn.bin", "wb") as f:
    f.write(data)
