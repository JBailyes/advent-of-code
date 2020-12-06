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
from vectors import Point, Vector
from itertools import combinations


class Moon:
    def __init__(self, start_pos, name):
        self.pos: Point = start_pos
        self.vel: Vector = Vector(0, 0, 0)
        self.name = name

    def p_energy(self):
        return abs(self.pos.x) + abs(self.pos.y) + abs(self.pos.z)

    def k_energy(self):
        return abs(self.vel.x) + abs(self.vel.y) + abs(self.vel.z)

    def total_energy(self):
        return self.p_energy() * self.k_energy()

    def __str__(self):
        return '{0}: {1} {2}'.format(self.name, self.pos, self.vel)


def main():
    colorama.init()

    inputFile = basename(__file__)[:2] + '-input.txt'
    lines = []
    with open(inputFile,  'r') as infile:
        for line in infile:
            lines.append(line.strip().strip("<>"))

    # lines = [
    #     'x = -1, y = 0, z = 2',
    #     'x = 2, y = -10, z = -7',
    #     'x = 4, y = -8, z = 8',
    #     ' x = 3, y = 5, z = -1'
    # ]
    #
    # lines = [
    #     'x=-8, y=-10, z=0',
    #     'x=5, y=5, z=10',
    #     'x=2, y=-7, z=3',
    #     'x=9, y=-8, z=-3'
    # ]

    moons = []
    names = 'abcd'
    for i in range(0, len(lines)):
        line = lines[i]
        name = names[i]
        x, y, z = re.compile('-?[0-9]+').findall(line)
        print('loaded:', x, y, z)
        moons.append(Moon(Point(int(x), int(y), int(z)), name))

    for step in range(1, 1001):
        print('step', step)
        for a, b in combinations(moons, 2):
            # print(a, b)
            if a.pos.x != b.pos.x:
                if a.pos.x > b.pos.x:
                    a.vel.x -= 1
                    b.vel.x += 1
                else:
                    a.vel.x += 1
                    b.vel.x -= 1
            if a.pos.y != b.pos.y:
                if a.pos.y > b.pos.y:
                    a.vel.y -= 1
                    b.vel.y += 1
                else:
                    a.vel.y += 1
                    b.vel.y -= 1
            if a.pos.z != b.pos.z:
                if a.pos.z > b.pos.z:
                    a.vel.z -= 1
                    b.vel.z += 1
                else:
                    a.vel.z += 1
                    b.vel.z -= 1
            # print('   ', a, b)

        energy = 0
        for moon in moons:
            moon.pos.x += moon.vel.x
            moon.pos.y += moon.vel.y
            moon.pos.z += moon.vel.z
            energy += moon.total_energy()
            if step % 100 == 0:
                print(moon)
        if step % 100 == 0:
            print('system energy', energy)
            print('')


if __name__ == "__main__":
    main()
