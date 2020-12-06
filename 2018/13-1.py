import argparse
import re
import string
from datetime import datetime
import operator


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('infile')
    args = parser.parse_args()

    layout = []
    y = 0
    with open(args.infile) as infile:
        for line in infile:
            if len(line.strip()) > 0:
                layout.append([])
                for char in line.rstrip('\n'):
                    layout[y].append(char)
                y += 1

    layoutHeight = len(layout)
    layoutWidth = len(layout[0])

    def getTrack(x, y):
        return layout[y][x]

    def printTrack():
        for row in layout:
            for track in row:
                print(track, end='')
            print()

    compass = ['<', '^', '>', 'v']

    class Truck:
        def __init__(self, x, y, direction):
            self.x = x
            self.y = y
            self.direction = direction
            self.turns = 0

        def move(self):
            self.moveInDirection(self.direction)
            newTrack = getTrack(self.x, self.y)
            self.setDirectionForTrack(newTrack)

        def moveInDirection(self, direction):
            vectorMap = {
                '>': [1, 0],
                '<': [-1, 0],
                '^': [0, -1],
                'v': [0, 1],
            }
            self.x += vectorMap[direction][0]
            self.y += vectorMap[direction][1]

        def setDirectionForTrack(self, trackType):
            currentDirection = self.direction
            curveMap = {
                '/': {
                    '>': '^',
                    '^': '>',
                    'v': '<',
                    '<': 'v',
                },
                '\\': {
                    '>': 'v',
                    '^': '<',
                    'v': '>',
                    '<': '^',
                },
            }
            if trackType in '/\\':
                self.direction = curveMap[trackType][currentDirection]
            elif trackType == '+':
                compassChange = [-1, 0, 1][self.turns % 3]
                currentCompassIndex = compass.index(self.direction)
                self.direction = compass[(currentCompassIndex + compassChange) % 4]
                self.turns = self.turns + 1

        def __str__(self):
            return self.direction

    trucks = []
    for y in range(0, layoutHeight):
        for x in range(0, layoutWidth):
            char = layout[y][x]
            if char in '<>^v':
                trucks.append(Truck(x, y, char))
                if x == 0 or x == layoutWidth - 1:
                    hiddenTrack = '|'
                elif y == 0 or y == layoutHeight - 1:
                    hiddenTrack = '-'
                else:
                    left = layout[y][x - 1]
                    right = layout[y][x + 1]
                    above = layout[y - 1][x]
                    below = layout[y + 1][x]
                    if left in '| ' or right in '| ':
                        hiddenTrack = '|'
                    elif above in '- ' or below in '- ':
                        hiddenTrack = '-'
                    elif left in '+' or right in '+':
                        hiddenTrack = '-'
                    elif above in '+' or below in '+':
                        hiddenTrack = '|'
                    else:
                        raise Exception("Can't work out what type of track is hidden at {0},{1}".format(x, y))
                layout[y][x] = hiddenTrack

    def getTrucks(x, y):
        trucksAtXY = []
        for truck in trucks:
            if (truck.x, truck.y) == (x, y):
                trucksAtXY.append(truck)
        return trucksAtXY

    crashed = False
    ticks = 0
    while not crashed:
        trucks.sort(key=operator.attrgetter('y', 'x'))
        for truck in trucks:
            truck.move()
            trucksAtNewLocation = getTrucks(truck.x, truck.y)
            if len(trucksAtNewLocation) > 1:
                crashed = True
                print('Crash at {0},{1}!'.format(truck.x, truck.y))

        ticks += 1
        print('Tick {0}'.format(ticks))
        if crashed:
            y = 0
            while y < layoutHeight:
                x = 0
                while x < layoutWidth:
                    trucksHere = getTrucks(x, y)
                    if len(trucksHere) == 1:
                        print(trucksHere[0], end='')
                    elif len(trucksHere) > 1:
                        print('X', end='')
                    else:
                        print(layout[y][x], end='')
                    x += 1
                print()
                y += 1
            print()

    print()
    print('Finish')


if __name__ == "__main__":
    main()
