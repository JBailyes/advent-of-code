import argparse
import os
import re


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

    programme = {}
    for line in lines:
        if line.startswith("mask = "):
            mask_str = line.removeprefix('mask = ')
            or_mask = int(mask_str.replace('X', '0'), 2)
            and_mask = int(mask_str.replace('X', '1'), 2)
        else:
            match = re.match(r'mem\[(\d+)] = (\d+)', line)
            address = int(match.group(1))
            loaded_value = int(match.group(2))
            print('loaded:', loaded_value)
            programme[address] = loaded_value & and_mask | or_mask
            print('mem[{}] = {}'.format(address, programme[address]))

    print('sum:', sum(programme.values()))


if __name__ == "__main__":
    main()
