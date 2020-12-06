import argparse
import re
import string
import time


def power(x, y, serialNumber):
    rackId = x + 10
    powerLevel = rackId * y
    powerLevel += serialNumber
    powerLevel *= rackId
    if powerLevel < 100:
        powerLevel = 0
    else:
        powerLevel = int(str(powerLevel)[-3])
    powerLevel -= 5
    return powerLevel


def threeByThreeSum(grid, x1, y1):
    total = 0
    for x in range(x1, x1 + 3):
        for y in range(y1, y1 + 3):
            # if y >= 295:
            #     print('grid[{0}][{1}]'.format(x, y))
            total += grid[x][y]
    return total


def sum(grid, x1, y1, size):
    total = 0
    for x in range(x1, x1 + size):
        for y in range(y1, y1 + size):
            total += grid[x][y]
    return total


def main():
    # Load the sequence
    parser = argparse.ArgumentParser()
    parser.add_argument('serialNumber')
    args = parser.parse_args()
    sn = int(args.serialNumber)

    grid = [[0]]
    for x in range(1, 301):
        grid.append([0])
        for y in range(1, 301):
            grid[x].append(power(x, y, sn))

    bestTotal = None
    bestCoords = None
    bestSize = None

    for size in range(1, 300):
        for x in range(1, 301 - size):
            for y in range(1, 301 - size):
                totalPower = sum(grid, x, y, size)
                if (x == 1 == y == size) or totalPower > bestTotal:
                    bestTotal = totalPower
                    bestCoords = (x, y)
                    bestSize = size

    bestX = bestCoords[0]
    bestY = bestCoords[1]

    print('sn: {0}'.format(sn))
    print('best total {0}'.format(bestTotal))
    print('best square cell is {0},{1} size {2}'.format(bestX, bestY, bestSize))
    print()
    for y in range(bestY, bestY + 3):
        for x in range(bestX, bestX + 3):
            print('{:4} '.format(grid[x][y]), end='')
        print()
    print()
    print()
    print('Finish')


if __name__ == "__main__":
    main()
