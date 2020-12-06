import argparse
import re
import string
from datetime import datetime
import operator
import sys
import colorama
from colorama import Fore, Back, Style
from copy import copy, deepcopy


class XY:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def up(self):
        return XY(self.x, self.y - 1)

    def down(self):
        return XY(self.x, self.y + 1)

    def left(self):
        return XY(self.x - 1, self.y)

    def right(self):
        return XY(self.x + 1, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        return (self.y < other.y) or (self.y == other.y and self.x < other.x)

    def __le__(self, other):
        return self.y < other.y or (self.y == other.y and self.x <= other.x)

    def __hash__(self):
        return self.y * 200 + self.x

    def __str__(self):
        return '{0}, {1}'.format(self.x, self.y)

    def __repr__(self):
        return '{0}.{1}'.format(self.x, self.y)


class Map:
    def __init__(self, mapData, width, height):
        self.grid = mapData
        self.width = width
        self.height = height

    def get(self, c):
        if c.x < 0 or c.x >= self.width or c.y < 0 or c.y >= self.height:
            value = None
        else:
            value = self.grid[c.y][c.x]
        return value

    def surrounding(self, c, type):
        values = [
            self.north(c), self.northEast(c), self.east(c), self.southEast(c),
            self.south(c), self.southWest(c), self.west(c), self.northWest(c)
        ]
        count = values.count(type)
        return count

    def north(self, c):
        return self.get(c.up())

    def northEast(self, c):
        return self.get(XY(c.x + 1, c.y - 1))

    def east(self, c):
        return self.get(c.right())

    def southEast(self, c):
        return self.get(XY(c.x + 1, c.y + 1))

    def south(self, c):
        return self.get(c.down())

    def southWest(self, c):
        return self.get(XY(c.x - 1, c.y + 1))

    def west(self, c):
        return self.get(c.left())

    def northWest(self, c):
        return self.get(XY(c.x - 1, c.y - 1))

    def all(self):
        for y in range(0, self.height):
            for x in range(0, self.width):
                yield (x, y, self.grid[y][x], XY(x, y))

    def set(self, c, value):
        self.grid[c.y][c.x] = value

    def resourceValue(self):
        woods = 0
        lumberyards = 0
        for x, y, value, c in self.all():
            if value == '|':
                woods += 1
            elif value == '#':
                lumberyards += 1
        resval = woods * lumberyards
        return resval

    def __str__(self):
        image = ''
        for y in range(0, self.height):
            image += '{0:,4}: '.format(y)
            for x in range(0, self.height):
                image += self.grid[y][x]
            image += '\n'
        return image

    def __repr__(self):
        return self.__str__()


def main():
    colorama.init()

    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()

    lines = []
    with open(args.input, 'r') as infile:
        for line in infile:
            lines.append(line.strip())

    width = len(lines[0])
    height = len(lines)

    mapData = {}
    for y in range(0, height):
        mapData[y] = {}
        for x in range(0, len(lines[y])):
            mapData[y][x] = lines[y][x]

    map = Map(mapData, width, height)

    def draw(map):
        for y in range(0, height):
            print('{0:5,}: '.format(y), end='')
            for x in range(0, width):
                c = XY(x, y)
                val = map.get(c)
                if val in '|':
                    print(Fore.GREEN, end='')
                elif val in '#':
                    print(Fore.RED, end='')
                print(val + Fore.RESET, end='')
            print()
    draw(map)
    print()

    def oneMinute(map):
        newMap = deepcopy(map)
        for x, y, value, c in map.all():
            if value == '.':
                trees = map.surrounding(c, '|')
                if trees >= 3:
                    newMap.set(c, '|')
            elif value == '|':
                lumberyards = map.surrounding(c, '#')
                if lumberyards >= 3:
                    newMap.set(c, '#')
            elif value == '#':
                trees = map.surrounding(c, '|')
                lumberyards = map.surrounding(c, '#')
                if trees >= 1 and lumberyards >= 1:
                    newMap.set(c, '#')
                else:
                    newMap.set(c, '.')
        return newMap

    prevResval = map.resourceValue()
    for m in range(0, 500):
        map = oneMinute(map)
        resval = map.resourceValue()
        change = resval - prevResval
        print('After {0} minutes: Resource value {1:,}, change of {2:,} from previous'.format(
            m + 1, resval, change))
        prevResval = resval

    draw(map)


    print()

    print()
    print('Finish')


if __name__ == "__main__":
    main()
