import argparse
import os


def main():
    day = os.path.basename(__file__).split('-')[0]
    challenge_input = '{}-input.txt'.format(day)
    # challenge_input = '{}-example-1.txt'.format(day)
    # challenge_input = '{}-example-2.txt'.format(day)

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
    runs_of_ones = []

    output = 0
    last_difference = -1
    for number in sorted_numbers:
        difference = number - output
        if difference == 1:
            if last_difference == 1:
                runs_of_ones[-1] += 1
            else:
                runs_of_ones.append(1)
        last_difference = difference

        print('{} -> {} = {}'.format(output, number, difference))
        output = number

    print(runs_of_ones)

    def sum_paths(run_length):
        """
        Run of 1: e.g. 4 5 = 1 path

        Run of 2: e.g. 4 5 6 = 2 paths
        4, 5, 6
        4,    6

        Run of 3: e.g. 4 5 6 7 = 4 paths
        4, 5, 6, 7
        4, 5,    7
        4,    6, 7
        4,       7
        """
        if run_length < 2:
            return 1
        if run_length == 2:
            return 2
        return sum_paths(run_length - 1) + sum_paths(run_length - 2) + sum_paths(run_length - 3)

    paths = 1
    for run_of_ones in runs_of_ones:
        paths *= sum_paths(run_of_ones)

    print('Paths:', paths)


if __name__ == "__main__":
    main()
