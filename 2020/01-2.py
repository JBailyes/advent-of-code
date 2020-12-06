import argparse
from itertools import combinations


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()

    lines = []
    with open(args.input, 'r') as infile:
        for line in infile:
            lines.append(int(line.strip()))

    for (x, y, z) in combinations(lines, 3):
        result = x + y + z
        if result == 2020:
            print('{} + {} + {} = {}'.format(x, y, z, result))
            print('{} * {} * {} = {}'.format(x, y, z, x * y * z))


if __name__ == "__main__":
    main()
