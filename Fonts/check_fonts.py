#!/usr/bin/env python

import json
from fontTools.ttLib import TTFont
import unicodedata
import os

import argparse

parser = argparse.ArgumentParser(description='Check if a character is in a font')
parser.add_argument('--charset', type=str, help='The charset file', default="chinese.txt")
parser.add_argument("--font_dir", type=str, help="The directory containing the fonts", default="./Fonts.orig")

args = parser.parse_args()

print(args)

fonts = []

for root,dirs,files in os.walk(args.font_dir):
    for file in files:
        if file.endswith(".ttf"):
            fonts.append(os.path.join(root, file))

with open(args.charset, encoding="utf-8") as f:
    charset = f.read()


def char_in_font(unicode_char, font):
    for cmap in font['cmap'].tables:
        if cmap.isUnicode():
            if ord(unicode_char) in cmap.cmap:
                return True
    return False

mm = {}

for fontpath in fonts:
    font = TTFont(fontpath)   # specify the path to the font in question
    mm[fontpath] = {
        "missing": [],
        "CoverRate": 0,
    }

    for char in charset:
        if char_in_font(char, font): continue
        # print(f"{fontpath} missing {char}, {unicodedata.name(char)}")
        mm[fontpath]["missing"].append({
            "char": char,
            "unicode": unicodedata.name(char),
        })
    mm[fontpath]["CoverRate"] = 1-len(mm[fontpath]["missing"])/len(charset)

with open("orig-font-missing-report.json", "w", encoding="utf8") as f:
    json.dump(mm, f, indent=2, ensure_ascii=False)
