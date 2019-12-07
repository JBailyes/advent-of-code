import argparse
import re
import string
from datetime import datetime
import operator
import sys
import colorama
from colorama import Fore, Back, Style
import math


def main():
    colorama.init()

    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()

    lines = []
    with open(args.input, 'r') as infile:
        for line in infile:
            lines.append(line.strip())
    # lines = ["1,0,0,0,99"]
    # lines = ["2,3,0,3,99"]
    # lines = ["2,4,4,5,99,0"]

    programme = []
    for code in lines[0].split(","):
        programme.append(int(code))
    programme[1] = 12
    programme[2] = 2

    pos = 0
    while pos < len(programme):
        op = programme[pos]
        if op == 99:
            print(programme)
            exit()
        addr1 = programme[pos + 1]
        addr2 = programme[pos + 2]
        addr3 = programme[pos + 3]
        if op == 1:
            result = programme[addr1] + programme[addr2]
        if op == 2:
            result = programme[addr1] * programme[addr2]
        programme[addr3] = result
        pos += 4

    # 1690717 - too low
    # 12490719

if __name__ == "__main__":
    main()
