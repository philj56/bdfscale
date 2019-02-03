#!/bin/env python3

import argparse

parser = argparse.ArgumentParser(description='Scale up a bdf font.')
parser.add_argument('file', type=str,
                    help='bdf file')
parser.add_argument('scale', type=int,
                    help='scale factor')
args = parser.parse_args()

# Lines that need all numbers scaled
scale_lines = [
        "DWIDTH",
        "SWIDTH",
        "BBX",
        "SIZE",
        "FONTBOUNDINGBOX",
        "PIXEL_SIZE",
        "POINT_SIZE",
        "RESOLUTION",
        "AVERAGE_WIDTH",
        "X_HEIGHT",
        "QUAD_WIDTH",
        "FONT_DESCENT",
        "FONT_ASCENT"
        ]

scale = args.scale
file = open(args.file)
bitmap = False
for line in file.readlines():
    if line.startswith("ENDCHAR"):
        bitmap = False
    elif bitmap:
        line = line.strip()
        pad = len(line) % 2
        line = line + "0"*pad  # Pad the line before we scale stuff
        size = len(line) * scale  # Calculate desired length of line

        # Do the actual scaling
        binary = bin(int(line.strip(), 16))[2:]
        rescaled = "".join([x*scale for x in binary])
        res = hex(int(rescaled, 2))[2:].upper()

        line = "0"*(size - len(res)) + res  # Pad out to desired length
        line = (line + "\n")*scale  # And correct number of lines
    elif any([line.startswith(x) for x in scale_lines]):
        words = line.split()
        for i, num in enumerate(words[1:]):
            words[i+1] = str(int(num) * scale)
        line = " ".join(words) + "\n"
    elif line.startswith("BITMAP"):
        bitmap = True
    print(line, end="")
