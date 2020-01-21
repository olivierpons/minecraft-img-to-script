# as of 2020/01/21, this should be saved in a location like:
# [your Minecraft folder]/[your world]/world-[Year]-[Month]-[day]/datapacks/...
#      ... /[name XX]/data/[name XX]/functions/[a name YY].mcfunction
# for example for me it's:
# my_test/world-2019-03-12/datapacks/hqf/data/hqf/functions/image.mcfunction
# and I call it like this in MineCraft:
# /function hqf:image
import argparse
import math
import sys
from pathlib import Path

from PIL import Image, UnidentifiedImageError


def distance(c1, c2):
    (r1, g1, b1) = c1
    (r2, g2, b2) = c2
    # return math.sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2)
    return math.sqrt(((r2-r1)*0.3) ** 2 + ((g2-g1)*0.59)**2 + ((b2-b1)*0.11)**2)


def usage():
    print('usage: python to_minecraft -i [input_file] -o [output_file]')
    sys.exit()


def main():
    parser = argparse.ArgumentParser(
        description='Image to Minecraft script converter.',
        allow_abbrev=True)
    parser.add_argument('-i', '--input', type=str, required=True,
                        help=f'input image file')
    parser.add_argument('-o', '--output', type=str, required=True,
                        help=f'output file')
    args = parser.parse_args()

    # make sure the image is an actual file:
    if not Path(args.input).is_file():
        print(f"File '{args.input}' is not a file.")
        parser.print_usage()
        sys.exit(2)

    # make sure the image is readable:
    try:
        with open(args.input):
            pass
    except IOError:
        print(f"File '{args.input}' is not readable.")
        parser.print_usage()
        sys.exit(2)

    # make sure we can read the image:
    try:
        im = Image.open(args.input)
    except UnidentifiedImageError:
        print(f"Could not read '{args.input}' (is it a real image?).")
        parser.print_usage()
        sys.exit(2)

    carpets = {(0xFF, 0xFF, 0xFF): "white_carpet",
               (0xF5, 0x79, 0x0F): "orange_carpet",
               (0xC8, 0x4D, 0xBE): "magenta_carpet",
               (0x46, 0xC1, 0xE4): "light_blue_carpet",
               (0xFE, 0xDA, 0x3D): "yellow_carpet",
               (0x7B, 0xC3, 0x13): "lime_carpet",
               (0xF4, 0x9D, 0xB8): "pink_carpet",
               (0x46, 0x4E, 0x51): "gray_carpet",
               (0x92, 0x93, 0x8C): "light_gray_carpet",
               (0x0F, 0x9A, 0x9A): "cyan_carpet",
               (0x89, 0x2E, 0xB8): "purple_carpet",
               (0x39, 0x40, 0xA9): "blue_carpet",
               (0x81, 0x51, 0x2D): "brown_carpet",
               (0x5D, 0x7B, 0x0F): "green_carpet",
               (0xAD, 0x28, 0x1F): "red_carpet",
               (0x00, 0x00, 0x00): "black_carpet", }

    colors = list(carpets.keys())

    width, height = im.size
    base_y = height // 2
    base_x = width // 2
    try:
        with open(args.output, 'w+') as f:
            f.write(f"fill ~{1+height-base_y} ~-1 "
                    f"~{-1-base_x} ~{-base_y} ~-1 ~{width-base_x} "
                    f"glass replace\n")
            for y in range(height):
                for x in range(width):
                    closest_colors = sorted(
                        colors, key=lambda color: distance(color,
                                                           im.getpixel((x, y))))
                    closest_color = closest_colors[0]
                    code = carpets[closest_color]
                    pos_y = (height - y) - base_y
                    pos_x = x - base_x
                    f.write(f"setblock ~{pos_y} ~ ~{pos_x} {code} replace\n")
    except FileNotFoundError:
        print(f"Could not write to: '{args.output}'.")
        parser.print_usage()
        sys.exit(2)


if __name__ == "__main__":
    main()
