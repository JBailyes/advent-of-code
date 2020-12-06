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

    for (x, y) in combinations(lines, 2):
        result = x + y
        if result == 2020:
            print(x, '+', y, '=', result)
            print(x, 'x', y, '=', x * y)

    # Answer: 259716


if __name__ == "__main__":
    main()
