import argparse
import re
import string
from datetime import datetime
import operator
import sys
import colorama
from colorama import Fore, Back, Style
import math


def calculate(modules):
    module_total = 0
    fuel_total = 0
    for mass in modules:
        module_fuel = math.floor(mass / 3.0) - 2
        module_total += module_fuel
        fuel_total += fuel_for_fuel(module_fuel)
    return module_total + fuel_total


def fuel_for_fuel(fuel_mass):
    needed = math.floor(fuel_mass / 3.0) - 2
    if needed <= 0:
        return 0
    return needed + fuel_for_fuel(needed)

def main():
    colorama.init()

    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()

    lines = []
    with open(args.input, 'r') as infile:
        for line in infile:
            lines.append(float(line.strip()))

    # 5076305 is wrong - too high
    # 88674296 is wrong - too high
    # 1689224 - wrong too low
    # 5073456 - was right
    print(calculate(lines))


if __name__ == "__main__":
    main()
