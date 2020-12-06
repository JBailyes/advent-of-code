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

    for y in range(0, maxY + 1):
        # print('{:3} |'.format(y), end='')
        for x in range(0, maxX + 1):
            closestDistance = maxX + maxY + 1
            closestPlaces = []
            placeStr = '.'
            for placeName, place in places.items():
                dist = manhattanDistance({'x': x, 'y': y}, place)
                if dist < closestDistance:
                    closestDistance = dist
                    closestPlaces = [placeName]
                elif dist == closestDistance:
                    closestPlaces.append(placeName)
            if len(closestPlaces) == 1:
                closestPlaceName = closestPlaces[0]
                places[closestPlaceName]['area'] += 1
                placeStr = closestPlaceName

            grid[x][y] = placeStr
            # if closestDistance == 0:
            #     print('{:>3}|'.format(closestPlaceName.upper()), end='')
            # else:
            #     print('{:3}|'.format(placeStr), end='')
        # print()

    for x in (0, maxX):
        for y in range(0, maxY):
            # print('checking {0},{1} for infinite area'.format(x,y))
            placeStr = grid[x][y]
            if placeStr in places.keys():
                del places[placeStr]
    for y in (0, maxY):
        for x in range(0, maxX):
            # print('checking {0},{1} for infinite area'.format(x,y))
            placeStr = grid[x][y]
            if placeStr in places.keys():
                del places[placeStr]

    print()
    biggestArea = 0
    for placeName, place in places.items():
        area = place['area']
        biggestArea = max(area, biggestArea)
        print('{0} area: {1}'.format(placeName, area))
    print()
    print('Biggest area is {0}'.format(biggestArea))
    print('Finish')


def manhattanDistance(a, b):
    return abs(a['x'] - b['x']) + abs(a['y'] - b['y'])


if __name__ == "__main__":
    main()
