import argparse
import re
import string
import time


class Marble:

    def __init__(self, number):
        if number == 0:
            self.counterClockwise = self
            self.clockwise = self
        else:
            self.counterClockwise = None
            self.clockwise = None
        self.number = number

    def getNumber(self):
        return self.number

    def setClockwise(self, marble):
        self.clockwise = marble

    def getClockwise(self, distance=1):
        if distance == 1:
            return self.clockwise
        else:
            return self.clockwise.getClockwise(distance - 1)

    def setCounterClockwise(self, marble):
        self.counterClockwise = marble

    def getCounterClockwise(self, distance=1):
        if distance == 1:
            return self.counterClockwise
        else:
            return self.counterClockwise.getCounterClockwise(distance - 1)

    def placeClockwiseOf(self, marble):
        self.counterClockwise = marble
        self.clockwise = marble.getClockwise()
        marble.setClockwise(self)
        self.clockwise.setCounterClockwise(self)

    def remove(self):
        self.counterClockwise.setClockwise(self.clockwise)
        self.clockwise.setCounterClockwise(self.counterClockwise)


def main():
    # Load the sequence
    parser = argparse.ArgumentParser()
    parser.add_argument('numPlayers')
    parser.add_argument('lastMarble')
    args = parser.parse_args()

    numPlayers = 424
    lastMarble = 71482

    numPlayers = int(args.numPlayers)
    lastMarble = int(args.lastMarble)

    currentMarble = Marble(0)
    nextMarbleNumber = 1
    nextMarble = Marble(nextMarbleNumber)

    scores = []

    for player in range(0, numPlayers):
        scores.append(0)

    # print(' {0}  '.format(0))
    while nextMarbleNumber <= lastMarble:
        for player in range(0, numPlayers):
            if nextMarbleNumber % 10000 == 0:
                print('Next marble: {0}'.format(format(nextMarbleNumber, ',d')))
            if nextMarbleNumber % 100000 == 0:
                time.sleep(5)
            if nextMarbleNumber > lastMarble:
                continue

            if nextMarbleNumber > 0 and nextMarbleNumber % 23 == 0:
                scores[player] += nextMarbleNumber
                sevenBack = currentMarble.getCounterClockwise(7)
                # print('seven back: {0}'.format(sevenBack.getNumber()))
                scores[player] += sevenBack.getNumber()
                currentMarble = sevenBack.getClockwise()
                sevenBack.remove()
            else:
                nextMarble.placeClockwiseOf(currentMarble.getClockwise())
                currentMarble = nextMarble

            nextMarbleNumber += 1
            nextMarble = Marble(nextMarbleNumber)

            # for i in range(0, len(circle)):
            #     if i == currentMarbleIndex:
            #         print('({0}) '.format(circle[i]), end='')
            #     else:
            #         print(' {0}  '.format(circle[i]), end='')
            # print()

    print()

    print('Winning score: {0}'.format(max(scores)))
    print('Finish')


def nextClockwise(circle, index):
    if index == len(circle) - 1:
        return 0
    else:
        return index + 1

def counterClockwise(circle, index, amount):
    if index >= amount:
        return index - amount
    return len(circle) - (amount - index)


if __name__ == "__main__":
    main()
