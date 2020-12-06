import argparse
import re
import string

opposites = {}
for letter in 'abcdefghijklmnopqrstuvwxyz':
    opposites[letter] = letter.upper()
    opposites[letter.upper()] = letter


def main():
    # Load the sequence
    parser = argparse.ArgumentParser()
    parser.add_argument('infile')
    args = parser.parse_args()

    lines = []
    with open(args.infile) as infile:
        for line in infile:
            lines.append(line.strip())

    # lines = [
    #     '1, 1',
    #     '1, 6',
    #     '8, 3',
    #     '3, 4',
    #     '5, 5',
    #     '8, 9'
    # ]

    placeNames = []
    for i in '12':
        for char in string.ascii_lowercase:
            placeNames.append(char + i)
    placeNames.reverse()

    places = {}

    maxX = 0
    maxY = 0
    for line in lines:
        (xStr, yStr) = line.split(',')
        x = int(xStr)
        y = int(yStr)
        maxX = max(maxX, x)
        maxY = max(maxY, y)
        placeName = placeNames.pop()
        places[placeName] = {'x': x, 'y': y, 'area': 0}

    grid = []
    for x in range(0, maxX + 1):
        grid.append([])
        for y in range(0, maxY + 1):
            grid[x].append(None)

    # print('     ', end='')
    # for x in range(0, maxX + 1):
    #     print('{:3} '.format(x), end='')
    # print()
    # print('    |', end='')
    # for x in range(0, maxX + 1):
    #     print('---+', end='')
    # print()

    maxDistance = 10000
    # maxDistance = 32
    areaSize = 0

    for y in range(0, maxY + 1):
        # print('{:3} |'.format(y), end='')
        for x in range(0, maxX + 1):
            totalProximity = 0
            for placeName, place in places.items():
                totalProximity += manhattanDistance({'x': x, 'y': y}, place)
            if totalProximity < maxDistance:
                grid[x][y] = '#'
                areaSize += 1
            else:
                grid[x][y] = ''
        #     print('{:3}|'.format(grid[x][y]), end='')
        # print()

    print()
    print('Size of area: {0}'.format(areaSize))
    print('Finish')


def manhattanDistance(a, b):
    return abs(a['x'] - b['x']) + abs(a['y'] - b['y'])


if __name__ == "__main__":
    main()
