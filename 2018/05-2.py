import argparse
import re


opposites = {}
for letter in 'abcdefghijklmnopqrstuvwxyz':
    opposites[letter] = letter.upper()
    opposites[letter.upper()] = letter


def main():
    # Load the sequence
    parser = argparse.ArgumentParser()
    parser.add_argument('infile')
    args = parser.parse_args()

    polyString = None
    with open(args.infile) as infile:
        for line in infile:
            polyString = line.strip()

    polyString = 'dabAcCaCBAcCcaDA'

    polymer = list(polyString)
    print(polymer)

    polymers = {}
    # for letter in 'abcdefghijklmnopqrstuvwxyz':
    for letter in 'abcABC':
        polymers[letter] = []
        for unit in polymer:
            if unit not in letter + letter.upper():
                polymers[letter].append(unit)

    shortest = len(polyString)

    for letter, polymer in polymers.items():
        reacted = True
        print(polymer)
        oldPolymer = polymer
        while reacted:
            newPolymer = react(oldPolymer)
            reacted = len(oldPolymer) != len(newPolymer)
            oldPolymer = newPolymer
        print(polymer)
        newPolymerLen = len(newPolymer)
        shortest = min(shortest, newPolymerLen)
        print('len without {0}: {1}'.format(letter, newPolymerLen))

    print('')
    print('Shortest: {0}'.format(shortest))

    print('Finish')


def react(polymer):
    # print(polymer)
    newPolymer = []
    lastIndex = len(polymer) - 1
    i = 0
    while i < lastIndex:
        left = polymer[i]
        right = polymer[i + 1]
        if left == opposites[right]:
            i += 2
            # print('  Eliminating {0}{1} from {2},{3}'.format(left, right, i-1, i))
        else:
            newPolymer.append(left)
            i += 1
    if i == lastIndex:
        newPolymer.append(polymer[lastIndex])
    return newPolymer


if __name__ == "__main__":
    main()
