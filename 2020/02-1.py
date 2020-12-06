import argparse
import re


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()

    lines = []
    with open(args.input, 'r') as infile:
        for line in infile:
            lines.append(line.strip())

    valid = 0

    for line in lines:
        match = re.match(r'(\d+)-(\d+) (.): (.*)', line)
        min = int(match.group(1))
        max = int(match.group(2))
        letter = match.group(3)
        password = match.group(4)

        occurrences = password.count(letter)
        if min <= occurrences <= max:
            valid += 1

    print('Valid passwords:', valid)


if __name__ == "__main__":
    main()
