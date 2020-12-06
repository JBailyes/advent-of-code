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

    lines = []
    with open(args.infile) as infile:
        for line in infile:
            lines.append(line.strip())

    # lines = [
    #     'dabAcCaCBAcCcaDA'
    # ]
    for line in lines:
        polymer = line
        reacted = True
        while reacted:
            newPolymer = react(polymer)
            reacted = polymer != newPolymer
            polymer = newPolymer
        print(polymer)
        print('len: {0}'.format(len(polymer)))

    print('Finish')


def react(polymer):
    # print(polymer)
    for i in range(1, len(polymer)):
        left = polymer[i-1]
        right = polymer[i]
        if left == opposites[right]:
            # print('  Eliminating {0}{1} from {2},{3}'.format(left, right, i-1, i))
            return polymer[0:max(i-1, 0)] + polymer[min(i+1, len(polymer) - 1):]
    return polymer


if __name__ == "__main__":
    main()
