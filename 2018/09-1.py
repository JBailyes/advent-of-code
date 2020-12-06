import argparse
import re
import string
import time

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

    nextMarble = 1
    scores = []
    currentMarbleIndex = 0
    circle = [0]

    for player in range(0, numPlayers):
        scores.append(0)

    # print(' {0}  '.format(0))
    while nextMarble <= lastMarble:
        for player in range(0, numPlayers):
            if nextMarble % 10000 == 0:
                print('Next marble: {0}'.format(format(nextMarble, ',d')))
            if nextMarble % 100000 == 0:
                time.sleep(5)
            if nextMarble > lastMarble:
                continue

            if nextMarble > 0 and nextMarble % 23 == 0:
                scores[player] += nextMarble
                removeIndex = counterClockwise(circle, currentMarbleIndex, 7)
                scores[player] += circle.pop(removeIndex)
                currentMarbleIndex = removeIndex % len(circle)
            else:
                currentMarbleIndex = nextClockwise(circle, currentMarbleIndex) + 1
                circle.insert(currentMarbleIndex, nextMarble)
            nextMarble += 1

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
