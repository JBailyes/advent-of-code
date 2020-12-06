import argparse
import re
import string
from datetime import datetime
import operator
import sys
import colorama
from colorama import Fore, Back, Style
from copy import copy


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


class Scan:
    def __init__(self, scanData, yMax, xMin, xMax):
        self.scan = scanData
        self.yMax = yMax
        self.xMin = xMin
        self.xMax = xMax

    def get(self, c):
        if c.x < self.xMin:
            for x in range(c.x, self.xMin):
                for y in range(0, self.yMax + 2):
                    self.scan[y][x] = '.'
            self.xMin = c.x
        elif c.x > self.xMax:
            for x in range(self.xMax + 1, c.x + 1):
                for y in range(0, self.yMax + 2):
                    self.scan[y][x] = '.'
            self.xMax = c.x
        value = self.scan[c.y][c.x]
        return value

    def getAbove(self, c):
        return self.get(c.up())

    def getBelow(self, c):
        return self.get(c.down())

    def getLeft(self, c):
        return self.get(c.left())

    def getRight(self, c):
        return self.get(c.right())

    def all(self):
        for y in range(0, self.yMax):
            for x in range(self.xMin, self.xMax + 1):
                yield (x, y, self.scan[y][x])

    def set(self, c, value):
        self.scan[c.y][c.x] = value

    def __str__(self):
        image = ''
        for y in range(0, self.yMax):
            image += '{0:,4}: '.format(y)
            for x in range(self.xMin, self.xMax + 1):
                image += self.scan[y][x]
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

    coordsReg = r'x=(\d+), y=(\d+)\.\.(\d+)|y=(\d+), x=(\d+)\.\.(\d+)'
    xMin = sys.maxsize
    xMax = 0
    yMax = 0

    for line in lines:
        match = re.match(coordsReg, line)
        if match.group(1) and match.group(2):
            x = int(match.group(1))
            y2 = int(match.group(3))
            xMin = min(x, xMin)
            xMax = max(x, xMax)
            yMax = max(y2, yMax)
        else:
            y = int(match.group(4))
            x1 = int(match.group(5))
            x2 = int(match.group(6))
            xMin = min(x1, xMin)
            xMax = max(x2, xMax)
            yMax = max(y, yMax)

    scanData = {}
    for y in range(0, yMax + 2):
        scanData[y] = {}
        for x in range(xMin, xMax + 1):
            scanData[y][x] = '.'
    scanData[0][500] = '+'

    for line in lines:
        match = re.match(coordsReg, line)
        if match.group(1) and match.group(2):
            x = int(match.group(1))
            y1 = int(match.group(2))
            y2 = int(match.group(3))
            for y in range(y1, y2 + 1):
                scanData[y][x] = '#'

        else:
            y = int(match.group(4))
            x1 = int(match.group(5))
            x2 = int(match.group(6))
            for x in range(x1, x2 + 1):
                scanData[y][x] = '#'

    # yMax = 71
    # xMax = 520
    print('Max y: {0}'.format(yMax))

    scan = Scan(scanData, yMax, xMin, xMax)

    def isContainedToLeft(coord):
        while True:
            if scan.get(coord.down()) in '~#':
                if scan.get(coord.left()) in '.~|':
                    coord = coord.left()
                elif scan.get(coord.left()) == '#':
                    return True
            else:
                return False

    def isContainedToRight(coord):
        while True:
            if scan.get(coord.down()) in '~#':
                if scan.get(coord.right()) in '.~|':
                    coord = coord.right()
                elif scan.get(coord.right()) == '#':
                    return True
            else:
                return False

    def isContained(coord):
        return isContainedToLeft(coord) and isContainedToRight(coord)

    def fill(coord):
        c = coord
        while scan.get(c) != '#':
            scan.set(c, '~')
            c = c.left()
        c = coord
        while scan.get(c) != '#':
            scan.set(c, '~')
            c = c.right()
    
    def overflowLeft(coord):
        c = coord
        newFlows = set()
        if c.y == yMax:
            return newFlows
        spreading = True
        while spreading and scan.get(c) != '#':
            if scan.get(c.down()) in '~#':
                scan.set(c, '|')
            elif scan.get(c.down()) == '.':
                scan.set(c, '|')
                spreading = False
                # flow(c.down())
                newFlows.add(c)
            elif scan.get(c.down()) == '|':
                # This overflow has already happened - don't duplicate
                return newFlows
            c = c.left()
        return newFlows
    
    def overflowRight(coord):
        c = coord
        newFlows = set()
        if c.y == yMax:
            return newFlows
        spreading = True
        while spreading and scan.get(c) != '#':
            if scan.get(c.down()) in '~#':
                scan.set(c, '|')
            elif scan.get(c.down()) == '.':
                scan.set(c, '|')
                spreading = False
                # flow(c.down())
                newFlows.add(c)
            elif scan.get(c.down()) == '|':
                # This overflow has already happened - don't duplicate
                return newFlows
            c = c.right()
        return newFlows

    def flow(source):
        c = source

        # Fall through sand and existing waterfall
        while c.y <= yMax and scan.get(c) in '.|':
            scan.set(c, '|')
            c = c.down()
        c = c.up()

        # if c.y >= yMax or c.x <= xMin or c.x >= xMax:
        if c.y >= yMax:
            return

        while isContained(c):
            fill(c)
            c = c.up()

        newFlows = set()
        newFlows |= overflowLeft(c)
        newFlows |= overflowRight(c)
        for newFlow in newFlows:
            flow(newFlow)

    flow(XY(500, 1))

    def draw():
        # printHeight = min(2000, scan.yMax)
        printHeight = scan.yMax
        for y in range(0, printHeight):
            print('{0:5,}: '.format(y), end='')
            for x in range(scan.xMin, scan.xMax + 1):
                c = XY(x, y)
                val = scan.get(c)
                if val in '~|':
                    print(Fore.CYAN, end='')
                print(val + Fore.RESET, end='')
            print()
    draw()

    water = 0
    for y in range(0, scan.yMax + 1):
        for x in range(scan.xMin, scan.xMax + 1):
            val = scanData[y][x]
            if val in '~':
                water += 1

    print()
    print('{0:,} settled water squares'.format(water))
    print('Finish')


if __name__ == "__main__":
    main()
