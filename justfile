
init:
    cd Texts/@old/case && protoc --python_out=.  ./yarn_spinner.proto
    cp Texts/@old/case/yarn_spinner_pb2.py Texts/@old/case/yarn_spinner.proto Texts/utils/
    openapi-generator-cli generate -i .github/workflows/paratranz-openapi.json -g python -o third/openapi-python

charset:
    python Texts/get_chars.py \
        --input-orig third/charset_orig.txt \
        --input-base third/chinese.txt \
        --input-base third/3500常用汉字.txt \
        --inputs Texts/@paraz-out \
        --output Texts/chinese.txt

fonts:
    rm -rf Fonts/@build
    cd Fonts && \
        python3 gen_fonts.py \
            --old-dir @old \
            --new-dir @new \
            --old-resS ../../@Dump/sharedassets0.assets.resS \
            --new-resS @new/sharedassets0.assets.resS \
            --out-dir @build

export:
    #!/usr/bin/env bash
    cd Texts
    rm -rf @paraz
    python text_io.py --export --raw @old --paraz @paraz --type serifu
    python text_io.py --export --raw @old --paraz @paraz --type m_text
    python text_io.py --export --raw @old --paraz @paraz --type charalist
    python text_io.py --export --raw @old --paraz @paraz --type spell
    python text_io.py --export --raw @old --paraz @paraz --type item
    python text_io.py --export --raw @old --paraz @paraz --type case
    python text_io.py --export --raw @old --paraz @paraz --type tooltips

paraz-out := "@paraz-out"
new := "@dist"
import:
    #!/usr/bin/env bash
    cd Texts
    rm -rf {{ new }}
    python text_io.py --import --raw @old --paraz {{ paraz-out }} --out {{ new }} --type serifu
    python text_io.py --import --raw @old --paraz {{ paraz-out }} --out {{ new }} --type m_text
    python text_io.py --import --raw @old --paraz {{ paraz-out }} --out {{ new }} --type charalist
    python text_io.py --import --raw @old --paraz {{ paraz-out }} --out {{ new }} --type spell
    python text_io.py --import --raw @old --paraz {{ paraz-out }} --out {{ new }} --type item
    python text_io.py --import --raw @old --paraz {{ paraz-out }} --out {{ new }} --type tooltips
    # python text_io.py --import --raw @old --paraz {{ paraz-out }} --out {{ new }} --type case
