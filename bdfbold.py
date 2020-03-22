#!/bin/env python3

import argparse

parser = argparse.ArgumentParser(description='Make a bdf font bold.')
parser.add_argument('file', type=str,
                    help='bdf file')
parser.add_argument('scale', type=int,
                    help='number of pixels to bolden by')
args = parser.parse_args()

scale = args.scale
file = open(args.file)
bitmap = False
for line in file.readlines():
    if line.startswith("WEIGHT_NAME"):
        line = 'WEIGHT_NAME "Bold"\n'
    if line.startswith("ENDCHAR"):
        bitmap = False
    elif bitmap:
        line = line.strip()
        pad = len(line) % 2
        line = line + "0"*pad  # Pad the line before we scale stuff

        leading = 0
        while leading < len(line) and line[leading] == "0":
            leading += 1

        # Do the actual scaling
        binary = bin(int(line.strip(), 16))[2:]
        bold = list(binary)
        for i, char in enumerate(binary[:scale]):
            for c in binary[:i]:
                bold[i] = str(int(c) | int(bold[i]))
        for i, char in enumerate(binary[scale:]):
            for c in binary[i:i+scale]:
                bold[i+scale] = str(int(c) | int(bold[i+scale]))
        bold += binary[-1] * scale + "0" * (8 - scale)
        res = hex(int("".join(bold), 2))[2:].upper()
        res = leading * "0" + res

        line = res + "0"*(len(res) % 2) # Pad out to desired length
        line += "\n"
    elif line.startswith("DWIDTH") or line.startswith("BBX"):
        words = line.split()
        words[1] = str(int(words[1]) + scale)
        line = " ".join(words) + "\n"
    elif line.startswith("BITMAP"):
        bitmap = True
    print(line, end="")
