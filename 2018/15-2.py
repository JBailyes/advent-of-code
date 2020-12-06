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


class Map:
    def __init__(self, lines):
        self.grid = []
        self.height = len(lines)
        self.width = len(lines[0])

        for y, line in enumerate(lines):
            self.grid.append([])
            for x, value in enumerate(line):
                self.grid[y].append(value)

    def get(self, c):
        if c.x < 0 or c.x >= self.width or c.y < 0 or c.y >= self.height:
            return None
        value = self.grid[c.y][c.x]
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
        for y in range(0, self.height):
            for x in range(0, self.width):
                yield (x, y, self.grid[y][x])

    def set(self, c, value):
        self.grid[c.y][c.x] = value

    def __str__(self):
        image = ''
        for y in range(0, self.height):
            for x in range(0, self.width):
                image += self.grid[y][x]
            image += '\n'
        return image

    def __repr__(self):
        return self.__str__()


class Unit:
    enemy = None

    def __init__(self, position):
        self.pos = position
        self.hitPoints = 200
        self.attackPower = 3

    def attack(self, other):
        other.takeHit(self.attackPower)
        # vectorMap = {
        #     XY(1, 0): '>',
        #     XY(-1, 0): '<',
        #     XY(0, -1): '^',
        #     XY(0, 1): 'v'
        # }
        # print('   Attack {0} {1} at {2}'.format(other, vectorMap[XY(
        #     other.pos.x - self.pos.x,
        #     other.pos.y - self.pos.y)],
        #     other.pos))

    def takeHit(self, magnitude):
        self.hitPoints -= magnitude

    def isDead(self):
        return self.hitPoints < 1

    def __repr__(self):
        return '{0}({1})'.format(self.__str__(), self.hitPoints)


class Elf(Unit):
    enemy = 'G'
    race = 'E'

    def __str__(self):
        return 'E'


class Goblin(Unit):
    enemy = 'E'
    race = 'G'

    def __str__(self):
        return 'G'


class ElfDeath(Exception):
    pass


def main():
    colorama.init()

    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()

    lines = []
    with open(args.input, 'r') as infile:
        for line in infile:
            lines.append(line.strip())

    map = Map(lines)
    mapCache = {}
    units = []

    def resetMapAndUnits():
        nonlocal map, mapCache, units

        map = Map(lines)
        mapCache = {}
        units = []

        for x, y, item in map.all():
            c = XY(x, y)
            if item == 'E':
                units.append(Elf(c))
            elif item == 'G':
                units.append(Goblin(c))

        units.sort(key=operator.attrgetter('pos'))

    # Find spaces in range of units of a type
    def inRangeOfType(unitType):
        inRange = set()
        for x, y, value in map.all():
            c = XY(x, y)
            if value == '.':
                surroundings = [map.getAbove(c), map.getBelow(c), map.getLeft(c), map.getRight(c)]
                if unitType in surroundings:
                    inRange.add(c)
        return inRange

    def getUnit(position):
        for unit in units:
            if unit.pos == position:
                return unit

    def findPaths(start, ends):
        if not ends:
            return []
        paths = [[start]]
        shortestPathsToEnd = []
        shortestDistanceToEnd = sys.maxsize
        prevRedundancies = []
        while paths:
            path = paths.pop(0)
            newLength = len(path) + 1
            if newLength > shortestDistanceToEnd:
                # If it's not going to be the shortest or joint shortest complete path then discard it
                continue
            currentSquare = path[-1]
            # Diverge in each direction
            for nextSquare in [currentSquare.up(), currentSquare.left(), currentSquare.right(), currentSquare.down()]:
                if map.get(nextSquare) != '.':
                    continue

                newPath = path.copy()
                newPath.append(nextSquare)

                if nextSquare in path:
                    # Discard the new path if it's looped or doubled-back on itself
                    continue

                if nextSquare in ends:
                    if newLength < shortestDistanceToEnd:
                        shortestPathsToEnd = [newPath]
                        shortestDistanceToEnd = newLength
                    elif newLength == shortestDistanceToEnd:
                        shortestPathsToEnd.append(newPath)
                    continue

                # If two paths have arrived at the same square then keep only the shortest per direction from start
                redundantPaths = []
                redundant = False
                for otherPath in paths:
                    if nextSquare == otherPath[-1]:
                        if newLength > len(otherPath):
                            redundant = True
                        else:
                            redundantPaths.append(otherPath)
                # If we end up at the same endpoint as a path previously made redundant then this one must be redundant
                for previousRedundancy in prevRedundancies:
                    if nextSquare == previousRedundancy[-1] and newLength >= len(previousRedundancy):
                        # Only remove redundancies for the same initial move
                        if previousRedundancy[1] == newPath[1]:
                            redundant = True
                            break
                for redundantPath in redundantPaths:
                    # Only remove redundancies for the same initial move
                    if redundantPath[1] == newPath[1]:
                        paths.remove(redundantPath)
                        prevRedundancies.append(redundantPath)
                if not redundant:
                    paths.append(newPath)
                else:
                    prevRedundancies.append(newPath)
        return shortestPathsToEnd

    def acquireTarget(unit):
        targetsInRange = []
        for c in [unit.pos.up(), unit.pos.left(), unit.pos.right(), unit.pos.down()]:
            if map.get(c) == unit.enemy:
                enemyUnit = getUnit(c)
                targetsInRange.append(enemyUnit)
        if targetsInRange:
            sortedTargets = sorted(targetsInRange, key=operator.attrgetter('hitPoints', 'pos'))
            target = sortedTargets[0]
            return target

    def assessUnit(unit):
        if unit.isDead():
            if unit.race == 'E':
                raise ElfDeath()
            map.set(unit.pos, '.')
            units.remove(unit)

    def moveUnit(unit):
        # If no positions have changed since last time then don't waste time trying to find a path
        if unit in mapCache:
            previousMap = mapCache[unit]
            currentMap = str(map)
            if currentMap == previousMap:
                # print('   No move available')
                # draw(unit, None)
                return False

        positionsInRangeOfTargets = inRangeOfType(unit.enemy)
        shortestPaths = findPaths(unit.pos, positionsInRangeOfTargets)
        if not shortestPaths:
            # print('   No move available')
            mapCache[unit] = str(map)
            # draw(unit, None)
            return False
        mapCache[unit] = None

        # Sort by the reachable square (the one at the end of the path), then the first move
        shortestPaths.sort(key=lambda path: (path[-1], path[1]))
        chosenPath = shortestPaths[0]
        oldPosition = chosenPath[0]
        newPosition = chosenPath[1]

        # Move along the chosen path
        map.set(oldPosition, '.')
        map.set(newPosition, str(unit))
        unit.pos = newPosition
        vectorMap = {
            XY(1, 0): '>',
            XY(-1, 0): '<',
            XY(0, -1): '^',
            XY(0, 1): 'v'
        }
        arrow = XY(
            newPosition.x - oldPosition.x,
            newPosition.y - oldPosition.y
        )
        # print('   Move {0} to {1}'.format(vectorMap[arrow], newPosition))
        # draw(unit, chosenPath)

        return True

    def draw(currentTurn=None, highlightPath=None):
        unitsInRow = []
        print('                 1 1 1 1 1 1 1 2 2')
        print('   0 2 4 6 7 8 9 0 2 4 6 7 8 9 0 1')
        for x, y, value in map.all():
            c = XY(x, y)
            if x == 0:
                if y % 2 == 0:
                    print('{0:>2} '.format(y), end='')
                else:
                    print('   ', end='')
            colours = {
                'G': Fore.LIGHTRED_EX,
                'E': Fore.LIGHTGREEN_EX,
                '.': Fore.LIGHTWHITE_EX,
                '#': Fore.LIGHTBLACK_EX
            }
            fc = colours[value]
            if currentTurn and c == currentTurn.pos:
                fc = Fore.YELLOW
            if highlightPath and c in highlightPath:
                print(Back.WHITE, end='')
                if currentTurn and c == currentTurn.pos:
                    fc = Fore.BLACK
            print(fc + value + Fore.RESET + Back.RESET, end='')
            if value in 'EG':
                unitsInRow.append(getUnit(c))
            if x == map.width - 1:
                print('   ', end='')
                for unit in unitsInRow:
                    print(' {0}({1})'.format(unit, unit.hitPoints), end='')
                unitsInRow = []
                print()
        print()

    def turn(unit):
        enemies = 0
        for other in units:
            if str(other) == unit.enemy:
                enemies += 1
        if not enemies:
            return False

        adjacentTarget = acquireTarget(unit)
        if adjacentTarget:
            unit.attack(adjacentTarget)
            # draw(unit, [adjacentTarget.pos])
            assessUnit(adjacentTarget)
        else:
            moved = moveUnit(unit)
            if not moved:
                return True
            adjacentTarget = acquireTarget(unit)
            if adjacentTarget:
                unit.attack(adjacentTarget)
                assessUnit(adjacentTarget)

        return True

    def round(roundsCount):
        # print('-- Round {0} -----------------------------------'.format(roundsCount))
        completed = True
        for unit in sorted(units, key=operator.attrgetter('pos')):
            if unit.isDead():
                continue
            # print('Turn of {0} from {1}:'.format(unit, unit.pos))
            completed = turn(unit)
            # draw()
            if not completed:
                return completed
        return completed

    def whoWon():
        return str(units[0])

    def score(fullRounds):
        totalHitPoints = 0
        for unit in units:
            totalHitPoints += unit.hitPoints
        finalScore = fullRounds * totalHitPoints
        return finalScore

    resetMapAndUnits()
    print('Start:')
    draw(None, None)

    def play(elfAttackPower):
        resetMapAndUnits()
        for unit in units:
            if type(unit) == Elf:
                unit.attackPower = elfAttackPower
        lastRoundCompleted = True
        roundsCount = 1
        while lastRoundCompleted:
            lastRoundCompleted = round(roundsCount)
            # draw()
            if not lastRoundCompleted:
                print('Game finished during round {0}'.format(roundsCount))
            # if roundsCount in [1, 2, 3, 23, 24, 25, 26, 27, 28, 47]:
            # if roundsCount in [24, 25, 26, 27, 28, 47]:
            #     print('After {0} rounds:'.format(roundsCount))
                finalScore = score(roundsCount - 1)
                return finalScore
            else:
                roundsCount += 1

    elfLosses = True
    elfAttackPower = 3
    while elfLosses:
        elfAttackPower += 1
        print('Elf attack power increased to {0}'.format(elfAttackPower))
        try:
            finalScore = play(elfAttackPower)
            elfLosses = False
            draw()
            print('Elves won with attack power {0}'.format(elfAttackPower))
            print('Score: {0:,}'.format(finalScore))
        except ElfDeath:
            print('   An Elf died')

    print()
    print('Finish')


if __name__ == "__main__":
    main()
