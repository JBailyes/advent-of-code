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
    total, length = subtreeTotal(numbers, 0)
    print()
    print('Total {0}'.format(total))

    print()
    print('Finish')


def subtreeTotal(numbers, index):
    metadataTotal = 0
    children = numbers[index]
    # print('c{0} '.format(children), end='')
    metadataEntries = numbers[index + 1]
    # print('m{0} '.format(metadataEntries), end='')
    position = index + 2
    numberCount = 2 + metadataEntries
    for i in range(0, children):
        (metadataSubtotal, subNumberCount) = subtreeTotal(numbers, position)
        metadataTotal += metadataSubtotal
        numberCount += subNumberCount
        position += subNumberCount
    print('c{0} '.format(children), end='')
    print('m{0} '.format(metadataEntries), end='')
    for i in range(position, position + metadataEntries):
        metadataTotal += numbers[i]
        print('n{0} '.format(numbers[i]), end='')
    print('t{0}'.format(metadataTotal))
    return metadataTotal, numberCount


if __name__ == "__main__":
    main()
