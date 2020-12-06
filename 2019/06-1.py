import argparse
import re
import string
from datetime import datetime
import operator
import sys
import colorama
from colorama import Fore, Back, Style
from os.path import basename
import math


orbits = {}


def orbit_count(orbiter):
    if orbiter not in orbits.keys():
        return 0
    orbited = orbits[orbiter]
    return 1 + orbit_count(orbited)


def main():
    colorama.init()

    inputFile = basename(__file__)[:2] + '-input.txt'
    lines = []
    with open(inputFile, 'r') as infile:
        for line in infile:
            lines.append(line.strip())

    # lines = [
    #     "COM)B",
    #     "B)C",
    #     "C)D",
    #     "D)E",
    #     "E)F",
    #     "B)G",
    #     "G)H",
    #     "D)I",
    #     "E)J",
    #     "J)K",
    #     "K)L"
    # ]

    for orbit in lines:
        inner, outer = orbit.split(")")
        print(outer + " orbits " + inner)
        orbits[outer] = inner

    orbits_total = 0
    for orbiter in orbits.keys():
        orbits_total += orbit_count(orbiter)

    print(orbits_total)


if __name__ == "__main__":
    main()
