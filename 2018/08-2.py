import argparse
import re
import string



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
    #     '2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2'
    # ]

    # print('Input: {0}'.format(lines[0]))
    numbers = []
    for numberStr in lines[0].split():
        numbers.append(int(numberStr))
    length, value = subtreeTotal(numbers, 0)
    print()
    print('Root value {0}'.format(value))

    print()
    print('Finish')


def subtreeTotal(numbers, index):
    value = 0
    children = numbers[index]
    print('c{0} '.format(children), end='')
    metadataEntries = numbers[index + 1]
    print('m{0} '.format(metadataEntries), end='')
    position = index + 2
    numberCount = 2 + metadataEntries
    childNodeValues = []
    for i in range(0, children):
        (subNumberCount, childValue) = subtreeTotal(numbers, position)
        numberCount += subNumberCount
        position += subNumberCount
        childNodeValues.append(childValue)
    # print('c{0} '.format(children), end='')
    # print('m{0} '.format(metadataEntries), end='')

    for i in range(position, position + metadataEntries):
        metadataNumber = numbers[i]
        print('m{0} '.format(metadataNumber), end='')
        if children == 0:
            value += metadataNumber
        else:
            if 0 < metadataNumber <= children:
                value += childNodeValues[metadataNumber - 1]
        print('v{0} '.format(value), end='')

    return numberCount, value


if __name__ == "__main__":
    main()
