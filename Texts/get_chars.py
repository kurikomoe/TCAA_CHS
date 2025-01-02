import argparse
import logging
from pathlib import Path
from typing import Set

import coloredlogs

coloredlogs.install(level='DEBUG')
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser()
parser.add_argument("--input-orig", help="basic charset file")
parser.add_argument("--input-base", help="basic charset file", nargs="*")
parser.add_argument("--inputs", help="collect all chars from path", required=True, nargs="*")
parser.add_argument("--output", help="output chinese.txt file", required=True)

args = parser.parse_args()
logger.info(args)

charset_orig: Set[str] = set()
charset: Set[str] = set()

def addTo(ss: str, target=charset):
    for ch in ss:
        target.add(ch)

for input_base in args.input_base:
    with open(input_base, "r", encoding="utf8") as f:
        data = f.read()
        addTo(data)
        addTo(data, target=charset_orig)

if args.input_orig:
    with open(args.input_orig, "r", encoding="utf8") as f:
        data = f.read()
        addTo(data)

# check whether the charset changed
charset_last_gen: Set[str] = set()
if Path(args.output).exists():
    with open(args.output, "r", encoding="utf8") as f:
        data = f.read()
        addTo(data, target=charset_last_gen)

for data_dir in args.inputs:
    logging.debug(f"Folder: {data_dir}")
    for file in Path(data_dir).glob("**/*.json"):
        logging.debug(f"reading {file}")
        with open(file, "r", encoding="utf8") as f:
            data = f.read()
        addTo(data)

charset_list = list(charset)
charset_list.sort()

# print("="*80)
# print("diff: ", charset - charset_orig)
# print("orig len: ", len(charset_orig))
# print("new  len: ", len(charset))

# input("cnt?")
# print("="*80)
# print(charset_list)
logging.info(f"Total Charset Length: {len(charset_list)}")

if charset_last_gen != charset:
    logging.warning("Charset Updated")
    charset_diff = charset - charset_last_gen
    logging.warning(f"New Chars: {charset_diff}")
    logging.warning(f"Diff Size: {len(charset_diff)}")
else:
    logging.info("Charset Unchanged")

with open(args.output, "w", encoding="utf8") as f:
    f.write("".join(charset_list))
