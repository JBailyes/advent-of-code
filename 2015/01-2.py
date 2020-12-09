import argparse
import os


def main():
    day = os.path.basename(__file__).split('-')[0]
    challenge_input = '{}-input.txt'.format(day)
    # challenge_input = '{}-example.txt'.format(day)

    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default=challenge_input)
    args = parser.parse_args()

    lines = []
    with open(args.input, 'r') as infile:
        for line in infile:
            lines.append(line.strip())

    def move(instruction):
        return {'(': 1, ')': -1}[instruction]

    line = lines[0]
    floor = 0
    for pos in range(len(line)):
        floor += move(line[pos])
        if floor == -1:
            print(pos + 1)
            exit()


if __name__ == "__main__":
    main()
