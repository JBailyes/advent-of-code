import argparse
import re
import string
from datetime import datetime
import operator
import sys
import colorama
from colorama import Fore,  Back,  Style
from os.path import basename
import math


orbits = {}


def orbit_path(orbiter):
    if orbiter not in orbits.keys():
        return set()
    orbited = orbits[orbiter]
    # return orbiter + '-' + orbit_path(orbited)
    return set([orbited]) | orbit_path(orbited)


def main():
    colorama.init()

    inputFile = basename(__file__)[:2] + '-input.txt'
    lines = []
    with open(inputFile,  'r') as infile:
        for line in infile:
            lines.append(line.strip())

    # lines = [
    #     "COM)B", "B)C", "C)D", "D)E", "E)F", "B)G", "G)H", "D)I", "E)J", "J)K", "K)L", "K)YOU", "I)SAN"
    # ]

    for orbit in lines:
        inner,  outer = orbit.split(")")
        orbits[outer] = inner

    # print(orbit_path('YOU'))
    # print(orbit_path('SAN'))

    transfers = orbit_path('YOU') ^ orbit_path('SAN')
    print(len(transfers))


if __name__ == "__main__":
    main()
