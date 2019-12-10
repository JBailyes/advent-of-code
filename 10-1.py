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

def main():
    colorama.init()

    inputFile = basename(__file__)[:2] + '-input.txt'
    # inputFile = '10-1-example-1.txt'
    # inputFile = '10-1-example-2.txt'
    # inputFile = '10-1-example-3.txt'
    # inputFile = '10-1-example-4.txt'
    # inputFile = '10-1-example-5.txt'
    lines = []
    with open(inputFile,  'r') as infile:
        for line in infile:
            lines.append(line.strip())

    width = len(lines[0])
    height = len(lines)
    asteroids = set()
    for y in range(0, height):
        for x in range(0, width):
            if lines[y][x] == '#':
                asteroids.add(Coord(x, y))

    best_sight = 0
    best_asteroid = None
    for asteroid in asteroids:
        # print(asteroid)
        sights = {}
        for other in asteroids:
            if asteroid == other:
                continue
            dx = other.x - asteroid.x
            dy = other.y - asteroid.y
            gcd = math.gcd(dx, dy)
            direction = Vector(dx/gcd, dy/gcd)
            sights[direction] = other
            # print('  ', other, ':', Coord(dx, dy), '=', direction)

        num_sight = len(sights)
        # print(num_sight)
        if num_sight > best_sight:
            best_sight = num_sight
            best_asteroid = asteroid

    print('best sight:', best_sight, 'from', best_asteroid)


class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return str(self.x) + ',' + str(self.y)


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return str(self.x) + ',' + str(self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(str(self.x) + ',' + str(self.y))


if __name__ == "__main__":
    main()
