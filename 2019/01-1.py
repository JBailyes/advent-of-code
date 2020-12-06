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

    total = 0
    for mass in lines:
        total += math.floor(float(mass) / 3.0) - 2

    print(total)

if __name__ == "__main__":
    main()
