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

    numbers = []
    for line in lines:
        numbers.append(int(line))

    sorted_numbers = sorted(numbers)
    sorted_numbers.append(sorted_numbers[-1] + 3)
    differences = {}
    output = 0
    for number in sorted_numbers:
        difference = number - output
        if difference not in differences.keys():
            differences[difference] = 0
        differences[difference] += 1
        print('{} -> {} = {}'.format(output, number, difference))
        output = number

    print(differences)
    print(differences[1] * differences[3])


if __name__ == "__main__":
    main()
