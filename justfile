
fonts:
    rm -rf Fonts/@build
    cd Fonts && \
        python3 gen_fonts.py \
            --old-dir @old \
            --new-dir @new \
            --old-resS ../@Dump/sharedassets0.assets.resS \
            --new-resS @new/sharedassets0.assets.resS \
            --out-dir @build
