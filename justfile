
init:
    python3 third/il2cpp-stringliteral-patcher/extract.py \
        -i Texts/@old/metadata/global-metadata.dat \
        -o Texts/@old/metadata/global-metadata.json
    cd Texts/@old/case && protoc --python_out=.  ./yarn_spinner.proto
    cp Texts/@old/case/yarn_spinner_pb2.py Texts/@old/case/yarn_spinner.proto Texts/utils/
    openapi-generator-cli generate -i .github/workflows/paratranz-openapi.json -g python -o third/openapi-python

charset:
    python Texts/get_chars.py \
        --input-orig third/charset_orig.txt \
        --input-base third/controller.txt \
        --input-base "third/Rus Letters.txt" \
        --inputs Texts/@paraz-out \
        --output Fonts/chinese.txt

fonts:
    rm -rf Fonts/@build
    # --old-resS ../../@Dump/sharedassets0.assets.resS
    cd Fonts && \
        python3 gen_fonts.py \
            --old-dir @old \
            --new-dir @new \
            --new-resS @new/sharedassets0.assets.resS \
            --out-dir @build
    # --old-resS @old/sharedassets0.assets.resS

paraz := "@paraz"
export:
    #!/usr/bin/env bash
    set -ex
    cd Texts
    rm -rf @paraz
    python text_io.py --export --raw @old --paraz {{ paraz }} --type serifu
    python text_io.py --export --raw @old --paraz {{ paraz }} --type m_text
    python text_io.py --export --raw @old --paraz {{ paraz }} --type charalist
    python text_io.py --export --raw @old --paraz {{ paraz }} --type spell
    python text_io.py --export --raw @old --paraz {{ paraz }} --type item
    python text_io.py --export --raw @old --paraz {{ paraz }} --type case
    python text_io.py --export --raw @old --paraz {{ paraz }} --type tooltips
    python text_io.py --export --raw @old --paraz {{ paraz }} --type location
    python text_io.py --export --raw @old --paraz {{ paraz }} --type courtroom
    python text_io.py --export --raw @old --paraz {{ paraz }} --type credits
    python text_io.py --export --raw @old --paraz {{ paraz }} --type save
    python text_io.py --export --raw @old --paraz {{ paraz }} --type inputs
    python text_io.py --export --raw @old --paraz {{ paraz }} --type episode
    python text_io.py --export --raw @old --paraz {{ paraz }} --type metadata

paraz-out := "@paraz-out"
new := "@dist"
import:
    #!/usr/bin/env bash
    set -ex
    cd Texts
    rm -rf {{ new }}
    python text_io.py --import --raw @old --paraz {{ paraz-out }} --out {{ new }} --type serifu
    python text_io.py --import --raw @old --paraz {{ paraz-out }} --out {{ new }} --type m_text
    python text_io.py --import --raw @old --paraz {{ paraz-out }} --out {{ new }} --type charalist
    python text_io.py --import --raw @old --paraz {{ paraz-out }} --out {{ new }} --type spell
    python text_io.py --import --raw @old --paraz {{ paraz-out }} --out {{ new }} --type item
    python text_io.py --import --raw @old --paraz {{ paraz-out }} --out {{ new }} --type tooltips
    python text_io.py --import --raw @old --paraz {{ paraz-out }} --out {{ new }} --type case
    python text_io.py --import --raw @old --paraz {{ paraz-out }} --out {{ new }} --type location
    python text_io.py --import --raw @old --paraz {{ paraz-out }} --out {{ new }} --type courtroom
    python text_io.py --import --raw @old --paraz {{ paraz-out }} --out {{ new }} --type credits
    python text_io.py --import --raw @old --paraz {{ paraz-out }} --out {{ new }} --type save
    python text_io.py --import --raw @old --paraz {{ paraz-out }} --out {{ new }} --type inputs
    python text_io.py --import --raw @old --paraz {{ paraz-out }} --out {{ new }} --type episode
    python text_io.py --import --raw @old --paraz {{ paraz-out }} --out {{ new }} --type metadata

    echo Rebuild global-metadata.dat
    mkdir -p @dist/il2cpp_data/Metadata
    python3 ../third/il2cpp-stringliteral-patcher/patch.py \
        -i @old/metadata/global-metadata.dat \
        -p @dist/global-metadata.patch.json \
        -o @dist/il2cpp_data/Metadata/global-metadata.dat.chs

    #-o @dist/global-metadata.dat.stage1

    # python3 ../scripts/patchMetaData.py \
    #     -t @dist/global-metadata.name.json \
    #     -i @dist/global-metadata.dat.stage1 \
    #     -o @dist/il2cpp_data/Metadata/global-metadata.dat.chs

    # cleanup
    rm -rf \
        @dist/global-metadata.name.json \
        @dist/global-metadata.patch.json \
        @dist/global-metadata.dat.stage1

sync:
    python3 ./scripts/downParatranz.py

native:
    ./scripts/sync_native.sh

[windows]
build:
    cd ./launcher
    xmake build
