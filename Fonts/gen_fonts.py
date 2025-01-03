import argparse
import io
import json
import logging
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

@dataclass
class FontDef:
    sdf: str
    atlas: str
    material: str
    ref: Optional["FontDef"] = None


ref = FontDef(
    sdf="OpenSans-Regular SDF-sharedassets0.assets-6.json",
    atlas="OpenSans-Regular SDF Atlas-sharedassets0.assets-3.json",
    material="OpenSans-Regular Atlas Material-sharedassets0.assets-2.json",
)

mapping = [
    FontDef(
        sdf="LiberationSans SDF-resources.assets-12429.json",
        atlas="LiberationSans SDF Atlas-resources.assets-761.json",
        material="LiberationSans SDF Material-resources.assets-103.json",
        ref = ref,
    ),
    FontDef(
        sdf="Merriweather-Regular Drop Thought Shadow-resources.assets-12434.json",
        atlas="Merriweather-Regular Atlas-resources.assets-762.json",
        material="Merriweather-Regular Atlas Material-resources.assets-106.json",
        ref = ref,
    ),
    FontDef(
        sdf="NotoSerifHK-Regular SDF-resources.assets-12435.json",
        atlas="NotoSerifHK-Regular Atlas-resources.assets-110.json",
        material="NotoSerifHK-Regular Atlas Material-resources.assets-1.json",
        ref = ref,
    ),
    FontDef(
        sdf="OpenSans-Medium SDF-sharedassets0.assets-134.json",
        atlas="OpenSans-Medium Atlas-sharedassets0.assets-16.json",
        material="OpenSans-Medium Atlas Material-sharedassets0.assets-12.json",
        ref = ref,
    ),
    FontDef(
        sdf="OpenSans-Regular SDF-sharedassets0.assets-135.json",
        atlas="OpenSans-Regular Atlas-sharedassets0.assets-36.json",
        material="OpenSans-Regular Atlas Material-sharedassets0.assets-14.json",
        ref = ref,
    ),
    FontDef(
        sdf="Raleway-Italic SDF-sharedassets0.assets-136.json",
        atlas="Raleway-Italic Atlas-sharedassets0.assets-17.json",
        material="Raleway-Italic Atlas Material-sharedassets0.assets-2.json",
        ref = ref,
    ),
    FontDef(
        sdf="Raleway-Regular SDF-sharedassets0.assets-137.json",
        atlas="Raleway-Regular Atlas-sharedassets0.assets-15.json",
        material="Raleway-Regular Atlas Material-sharedassets0.assets-11.json",
        ref = ref,
    ),
    FontDef(
        sdf="Raleway-SemiBold SDF-sharedassets0.assets-138.json",
        atlas="Raleway-SemiBold Atlas-sharedassets0.assets-34.json",
        material="Raleway-SemiBold Atlas Material-sharedassets0.assets-3.json",
        ref = ref,
    ),

    FontDef(
        sdf="Typewriter-resources.assets-12437.json",
        atlas="OpenSans-Medium Atlas-resources.assets-109.json",
        material="OpenSans-Medium Atlas Material-resources.assets-105.json",
        ref = ref,
    ),
    FontDef(
        sdf="Title-resources.assets-12436.json",
        atlas="Title Atlas-resources.assets-763.json",
        material="Merriweather-Regular Atlas Material-resources.assets-107.json",
        ref = ref,
    ),
    # FontDef(
    #     sdf="",
    #     atlas="",
    #     material="",
    #     ref = ref,
    # ),
]


parser = argparse.ArgumentParser()
parser.add_argument("--old-dir", required=True, help="the old font file name, like `OpenSans-Regular`")
parser.add_argument("--new-dir", required=True, help="the new gen font file name")
parser.add_argument("--out-dir", required=True, help="the output folder")

parser.add_argument("--old-resS", required=True, help="the resS file")
parser.add_argument("--new-resS", required=True, help="the resS file")

args = parser.parse_args()

print(args)

with open(args.old_resS, "rb") as f:
    out_resS_bin = f.read()
    out_resS = io.BytesIO(out_resS_bin)

with open(args.new_resS, "rb") as f:
    new_resS_bin = f.read()
    new_resS = io.BytesIO(new_resS_bin)


old_root = Path(args.old_dir)
new_root = Path(args.new_dir)

Path(args.out_dir).mkdir(parents=True, exist_ok=True)
out_resS_path = Path(args.out_dir) / "sharedassets0.assets.resS"

def find_file_by_regex(root: Path, pat):
    return [f for f in os.listdir(root) if re.match(pat, f)]

def DictCopyAttr(key, dst, src):
    keys = key.split(".")

    # Retrieve the value from the source dictionary
    try:
        tmp1 = src
        for k in keys:
            tmp1 = tmp1[k]
    except KeyError:
        print(f"Old Key '{k}' not found")
        print(f"Available keys: {list(tmp1.keys())}")
        return

    # Navigate to the destination and set the value
    try:
        tmp2 = dst
        for k in keys[:-1]:  # Stop at the second-to-last key
            if k not in tmp2:
                tmp2[k] = {}  # Create nested dictionaries as needed
            tmp2 = tmp2[k]

        tmp2[keys[-1]] = tmp1  # Set the final key's value
    except Exception as e:
        print(f"Failed to set value in destination: {e}")
        return

    return


def process_sdf(old_root: Path, old_sdf, new_root: Path, new_sdf, output: Path):
    old_file_path = old_root / old_sdf
    new_file_path = new_root / new_sdf

    old_file_data = json.load(open(old_file_path, 'r', encoding="utf8"))
    new_file_data = json.load(open(new_file_path, 'r', encoding="utf8"))

    DictCopyAttr("m_Name", new_file_data, old_file_data)
    DictCopyAttr("m_GameObject", new_file_data, old_file_data)
    DictCopyAttr("m_Script", new_file_data, old_file_data)
    DictCopyAttr("m_Name", new_file_data, old_file_data)
    DictCopyAttr("material", new_file_data, old_file_data)
    DictCopyAttr("m_SourceFontFile", new_file_data, old_file_data)
    DictCopyAttr("m_SourceFontFileGUID", new_file_data, old_file_data)
    DictCopyAttr("m_FaceInfo.m_FamilyName", new_file_data, old_file_data)
    DictCopyAttr("m_FaceInfo.m_StyleName", new_file_data, old_file_data)
    DictCopyAttr("m_AtlasTextures", new_file_data, old_file_data)

    # out: Path = output / "sdf"
    out: Path = output
    out.mkdir(parents=True, exist_ok=True)
    out = out / old_sdf

    json.dump(new_file_data, open(out, "w", encoding="utf8"), ensure_ascii=False, indent=2)
    return

def process_material(old_root: Path, old_material, new_root: Path, new_material, output: Path):
    old_file_path = old_root / old_material
    new_file_path = new_root / new_material

    old_file_data = json.load(open(old_file_path, 'r', encoding="utf8"))
    new_file_data = json.load(open(new_file_path, 'r', encoding="utf8"))

    DictCopyAttr("m_Name", new_file_data, old_file_data)
    DictCopyAttr("m_Shader", new_file_data, old_file_data)

    FoundFlag = False
    _mainTex_m_Texture = None
    for item in old_file_data["m_SavedProperties"]["m_TexEnvs"]["Array"]:
        if item["first"] == "_MainTex":
            _mainTex_m_Texture = item["second"]["m_Texture"]
            break

    for item in new_file_data["m_SavedProperties"]["m_TexEnvs"]["Array"]:
        if item["first"] == "_MainTex":
            item["second"]["m_Texture"] = _mainTex_m_Texture
            FoundFlag = bool(True and _mainTex_m_Texture)
            break
    assert FoundFlag

    out = output / old_material
    json.dump(new_file_data, open(out, "w", encoding="utf8"), ensure_ascii=False, indent=2)
    return


atlas_cache = {}
def process_atlas(old_root: Path, old_atlas, new_root: Path, new_atlas, output: Path):
    global atlas_cache

    new_atlas_path = new_root / new_atlas
    new_atlas_data = json.load(open(new_atlas_path, "r", encoding="utf8"))

    assert "m_StreamData" in new_atlas_data

    offset = new_atlas_data["m_StreamData"]["offset"]
    size = new_atlas_data["m_StreamData"]["size"]

    new_resS.seek(offset, io.SEEK_SET)
    data = new_resS.read(size)

    # ============  Solution1: embeded ================
    # data_bytes = list(data)
    # new_atlas_data["image data"] = data_bytes
    # new_atlas_data["m_StreamData"] = {
    #     "offset": 0,
    #     "size": 0,
    #     "path": ""
    # }
    # old_file_path = old_root / old_atlas
    # old_file_data = json.load(open(old_file_path, 'r', encoding="utf8"))

    # DictCopyAttr("m_Name", new_atlas_data, old_file_data)
    # DictCopyAttr("m_IsReadable", new_atlas_data, old_file_data)

    # out = output / old_atlas
    # json.dump(new_atlas_data, open(out, "w", encoding="utf8"), ensure_ascii=False, indent=2)


    # ============  Solution2: write to resS ================
    if (offset, size) not in atlas_cache:
        new_offset = out_resS.seek(0, io.SEEK_END)
        out_resS.write(data)
        atlas_cache[(offset, size)] = (new_offset, size)
    else:
        new_offset, size = atlas_cache[(offset, size)]

    new_atlas_data["image data"] = []
    new_atlas_data["m_StreamData"]["offset"] = new_offset
    new_atlas_data["m_StreamData"]["size"] = size

    old_file_path = old_root / old_atlas
    old_file_data = json.load(open(old_file_path, 'r', encoding="utf8"))

    DictCopyAttr("m_Name", new_atlas_data, old_file_data)

    out = output / old_atlas
    json.dump(new_atlas_data, open(out, "w", encoding="utf8"), ensure_ascii=False, indent=2)

    return


output = Path(args.out_dir)

for font_def in mapping:
    print(font_def)

    assert font_def.ref
    process_sdf(old_root, font_def.sdf, new_root, font_def.ref.sdf, output)
    process_material(old_root, font_def.material, new_root, font_def.ref.material, output)
    process_atlas(old_root, font_def.atlas, new_root, font_def.ref.atlas, output)


# ============  Solution2: write to resS ================
with open(out_resS_path, "wb") as fout:
    out_resS.seek(0, io.SEEK_SET)
    fout.write(out_resS.read())
