import argparse
import itertools
import os
import re


def main():
    day = os.path.basename(__file__).split('-')[0]
    challenge_input = '{}-input.txt'.format(day)
    # challenge_input = '{}-example-2.txt'.format(day)

    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default=challenge_input)
    args = parser.parse_args()

    lines = []
    with open(args.input, 'r') as infile:
        for line in infile:
            lines.append(line.strip())

    bit_masks = [2 ** n for n in range(36)]

    programme = {}
    for line in lines:
        if line.startswith("mask"):
            mask_str = line.removeprefix('mask = ')
            x_bits = []
            floaters = []
            for i in range(36):
                if mask_str[35 - i] == 'X':
                    x_bits.append(i)
            all_set = 2 ** (len(x_bits) + 1) - 1
            for combo in range(2 ** len(x_bits)):  # All possible combinations of 1s and 0s, as decimal integers
                combo_or_mask = 0
                combo_and_mask = all_set
                combo_str = '{0:b}'.format(combo)
                for i in range(len(x_bits)):
                    x_bit_to_set = x_bits[i]
                    x_bit_mask = bit_masks[x_bit_to_set]
                    if combo & bit_masks[i]:
                        # Set this position to a 1
                        combo_or_mask |= x_bit_mask
                    else:
                        # Set this position to a 0
                        combo_and_mask ^= x_bit_mask
                floaters.append((combo_or_mask, combo_and_mask))
            main_or_mask = int(mask_str.replace('X', '0'), 2)

        else:
            match = re.match(r'mem\[(\d+)] = (\d+)', line)
            masked_address = int(match.group(1)) | main_or_mask
            value = int(match.group(2))
            for or_mask, and_mask in floaters:
                address = masked_address & and_mask | or_mask
                programme[address] = value

    # 2506753223342 is too low
    print('sum:', sum(programme.values()))


if __name__ == "__main__":
    main()
