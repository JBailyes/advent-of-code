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
    # inputFile = '10-2-example-1.txt'
    # inputFile = '10-1-example-2.txt'
    # inputFile = '10-1-example-3.txt'
    # inputFile = '10-1-example-4.txt'
    # inputFile = '10-1-example-5.txt'
    lines = []
    with open(inputFile,  'r') as infile:
        for line in infile:
            lines.append(line.strip())

    station = Coord(29, 28)
    # station = Coord(8, 3)
    # station = Coord(11, 13)

    width = len(lines[0])
    height = len(lines)
    asteroids = set()
    for y in range(0, height):
        for x in range(0, width):
            if lines[y][x] == '#':
                asteroid = Coord(x, y)
                if asteroid != station:
                    asteroids.add(asteroid)

    sights = {}
    for asteroid in asteroids:
        dx = asteroid.x - station.x
        dy = asteroid.y - station.y
        gcd = math.gcd(dx, dy)
        direction = Vector(dx/gcd, dy/gcd)
        if direction not in sights:
            sights[direction] = []
        sights[direction].append(Vector(dx, dy))
        # print('  ', other, ':', Coord(dx, dy), '=', direction)

    for direction in sights.keys():
        sights[direction].sort(key=Vector.magnitude)
        print(int(direction.time()), ':', sights[direction])

    print('clock:', sorted(sights.keys(), key=Vector.time))

    print('firing lazer')
    blitz_count = 0
    while len(sights) > 0:
        for direction in sorted(sights.keys(), key=Vector.time):
            vect = sights[direction].pop(0)
            if len(sights[direction]) == 0:
                del sights[direction]
            blitz_count += 1
            if blitz_count == 200:
                target = Coord(station.x + vect.x, station.y + vect.y)
                print('vaporised', blitz_count, target)
                print(target.x * 100 + target.y)


class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return str(self.x) + ',' + str(self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(str(self.x) + ',' + str(self.y))


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def normalised(self):
        gcd = math.gcd(self.x, self.y)
        return Vector(self.x / gcd, self.y / gcd)

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)

    def angle(self, other):
        return math.degrees(
            math.acos(
                self.dot(other) / (self.magnitude() * other.magnitude())))

    def time(self):
        noon = Vector(0, -1)
        small_angle = noon.angle(self)
        angle = small_angle
        if self.x < 0:
            angle = 360 - small_angle
        return angle

    def __str__(self):
        return str(self.x) + ',' + str(self.y)

    def __repr__(self):
        return '(' + self.__str__() + ')'

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(str(self.x) + ',' + str(self.y))


if __name__ == "__main__":
    main()
