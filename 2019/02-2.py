import argparse
import re
import string
from datetime import datetime
import operator
import sys
import colorama
from colorama import Fore, Back, Style
import math


def run(programme, param1, param2):
    programme[1] = param1
    programme[2] = param2
    pos = 0
    while pos < len(programme):
        op = programme[pos]
        if op == 99:
            return programme[0]
        addr1 = programme[pos + 1]
        addr2 = programme[pos + 2]
        addr3 = programme[pos + 3]
        if op == 1:
            result = programme[addr1] + programme[addr2]
        if op == 2:
            result = programme[addr1] * programme[addr2]
        programme[addr3] = result
        pos += 4


def main():
    colorama.init()

    # parser = argparse.ArgumentParser()
    # parser.add_argument('input')
    # args = parser.parse_args()

    lines = []
    with open('02-input.txt', 'r') as infile:
        for line in infile:
            lines.append(line.strip())

    programme = []
    for code in lines[0].split(","):
        programme.append(int(code))

    target = 19690720
    for noun in range(0, 99):
        for verb in range(0, 99):
            result = run(programme.copy(), noun, verb)
            if result == target:
                print(100 * noun + verb)
                exit()

    # 2003

if __name__ == "__main__":
    main()
