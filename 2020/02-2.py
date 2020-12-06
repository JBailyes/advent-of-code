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
        index1 = int(match.group(1)) - 1
        index2 = int(match.group(2)) - 1
        letter = match.group(3)
        password = match.group(4)

        matches = 0
        if len(password) > index1 and password[index1] == letter:
            matches += 1

        if len(password) > index2 and password[index2] == letter:
            matches += 1

        if matches == 1:
            valid += 1

    print('Valid passwords:', valid)


if __name__ == "__main__":
    main()
