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


def tracePath(path):
    pathCoords = set()
    pathSteps = {}

    centralPort = {'x': 0, 'y': 0}
    stepCount = 0
    prev = centralPort
    for move in path:
        direction = move[:1]
        size = int(move[1:])
        for i in range(0, size):
            if direction == 'U':
                xFact = 0
                yFact = 1
            if direction == 'D':
                xFact = 0
                yFact = -1
            if direction == 'L':
                xFact = -1
                yFact = 0
            if direction == 'R':
                xFact = 1
                yFact = 0

            x = prev['x'] + 1 * xFact
            y = prev['y'] + 1 * yFact
            coord = str(x) + ',' + str(y)
            # print(coord)
            pathCoords.add(coord)
            prev = {'x': x, 'y': y}

            stepCount += 1
            if coord not in pathSteps:
                pathSteps[coord] = stepCount

    return pathCoords, pathSteps


def main():
    colorama.init()

    inputFile = basename(__file__)[:2] + '-input.txt'
    lines = []
    with open(inputFile, 'r') as infile:
        for line in infile:
            lines.append(line.strip())

    # lines = [
    #     "R75,D30,R83,U83,L12,D49,R71,U7,L72",
    #     "U62,R66,U55,R34,D71,R55,D58,R83"
    # ]
    # lines = [
    #     "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51",
    #     "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"
    # ]
    # lines = ["R8,U5,L5,D3", "U7,R6,D4,L4"]

    path1 = []
    path2 = []
    for move in lines[0].split(','):
        path1.append(move)
    for move in lines[1].split(','):
        path2.append(move)

    pathCoords1, pathSteps1 = tracePath(path1)
    pathCoords2, pathSteps2 = tracePath(path2)

    shortest = 1000000
    crossovers = pathCoords1 & pathCoords2
    for crossover in crossovers:
        across = abs(int(crossover.split(',')[0]))
        up = abs(int(crossover.split(',')[1]))
        dist = across + up
        steps = pathSteps1[crossover] + pathSteps2[crossover]
        # print(steps)
        if 0 < steps < shortest:
            shortest = steps

    print(shortest)

    # 7388


if __name__ == "__main__":
    main()
