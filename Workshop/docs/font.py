import os

from PIL import Image, ImageDraw, ImageFont

TEST_TEXT = "房 骨 告 曜 门 复 刃 径 画"

FONTS = [
    {
        "name": "Noto Serif CJK (Default), most time fallback to jp",
        "path": "NotoSerifCJK.ttc",
    },
    {
        "name": "Noto Serif SC (Simplified Chinese)",
        "path": "NotoSerifCJKsc-Regular.otf",
    },
    {
        "name": "Noto Serif TC HK (Traditional Chinese, HongKong)",
        "path": "NotoSerifCJKhk-Regular.otf",
    },
    {
        "name": "Noto Serif TC TW (Traditional Chinese, Taiwan)",
        "path": "NotoSerifCJKtc-Regular.otf",
    },
    {
        "name": "Noto Serif JP (Japanese)",
        "path": "NotoSerifCJKjp-Regular.otf",
    }
]

FONT_SIZE = 60
LABEL_FONT_SIZE = 36
IMAGE_WIDTH = 1000
PADDING = 40
LABEL_TO_TEXT_SPACING = 10
BLOCK_SPACING = 50


def create_comparison_image():
    try:
        label_font = ImageFont.truetype("arial.ttf", LABEL_FONT_SIZE)
    except IOError:
        try:
            label_font = ImageFont.truetype(FONTS[0]["path"], LABEL_FONT_SIZE)
        except IOError:
            label_font = ImageFont.load_default()
            print("Warning: Could not load a proper label font. Using default tiny font.")

    total_height = PADDING
    for font_info in FONTS:
        total_height += LABEL_FONT_SIZE + LABEL_TO_TEXT_SPACING
        total_height += FONT_SIZE + BLOCK_SPACING
    total_height += PADDING

    img = Image.new('RGB', (IMAGE_WIDTH, total_height), color='white')
    draw = ImageDraw.Draw(img)

    current_y = PADDING

    for font_info in FONTS:
        font_path = font_info["path"]
        font_name = font_info["name"]

        draw.text((PADDING, current_y), font_name, font=label_font, fill='blue')
        current_y += LABEL_FONT_SIZE + LABEL_TO_TEXT_SPACING

        if os.path.exists(font_path):
            try:
                cjk_font = ImageFont.truetype(font_path, FONT_SIZE)
                draw.text((PADDING, current_y), TEST_TEXT, font=cjk_font, fill='black')
            except Exception as e:
                draw.text((PADDING, current_y), f"Error loading font: {e}", font=label_font, fill='red')
        else:
            draw.text((PADDING, current_y), f"Font file not found: {font_path}", font=label_font, fill='red')

        current_y += FONT_SIZE + BLOCK_SPACING

    output_filename = "cjk_variants_comparison.png"
    img.save(output_filename)
    print(f"Comparison image saved as {output_filename}")

if __name__ == "__main__":
    create_comparison_image()
