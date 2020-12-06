import argparse
import re
import string
import time
from datetime import datetime


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


def sum(grid, x1, y1, sizeX, sizeY):
    total = 0
    for x in range(x1, x1 + sizeX):
        for y in range(y1, y1 + sizeY):
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

    for size in range(1, 301):
    # for size in range(3, 4):
        print('size: {0}, '.format(size), end='')
        sizeStart = datetime.now()

        for x in range(1, 301 - size):
            for y in range(1, 301 - size):
                if x == 1 and y == 1:
                    totalPower = sum(grid, x, y, size, size)
                    prevY1Total = totalPower
                    prevTotal = totalPower
                else:
                    if y == 1:
                        # Subtract 1st col from prev square
                        totalPower = prevY1Total - sum(grid, x - 1, y, 1, size)
                        # Add last col of new square
                        totalPower += sum(grid, x + size - 1, y, 1, size)
                        prevY1Total = totalPower
                        prevTotal = totalPower
                    else:
                        # Subtract 1st row from prev square
                        totalPower = prevTotal - sum(grid, x, y - 1, size, 1)
                        # Add last row of new square
                        totalPower += sum(grid, x, y + size - 1, size, 1)
                        prevTotal = totalPower

                # if (x == 1 == y == size) or totalPower > bestTotal:
                if not bestTotal or totalPower > bestTotal:
                    bestTotal = totalPower
                    bestCoords = (x, y)
                    bestSize = size
        sizeDuration = datetime.now() - sizeStart
        print(' {0:,.2f} seconds'.format(sizeDuration.total_seconds()))

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
