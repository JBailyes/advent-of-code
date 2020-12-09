import argparse
from itertools import combinations


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('preamble')
    args = parser.parse_args()

    lines = []
    with open(args.input, 'r') as infile:
        for line in infile:
            lines.append(line.strip())

    numbers = []
    for line in lines:
        numbers.append(int(line))

    preamble = int(args.preamble)
    for current_index in range(preamble, len(numbers)):
        current_number = numbers[current_index]
        print('numbers[{}]: {}'.format(current_index, current_number))
        options = set(numbers[current_index - preamble:current_index])
        # print('preamble:', options)
        rule_holds = False
        for pair in combinations(options, 2):
            sum = pair[0] + pair[1]
            if sum == current_number:
                print('   {} + {} = {}'.format(pair[0], pair[1], sum))
                rule_holds = True
                break
        if not rule_holds:
            print('{} breaks the rule'.format(current_number))
            break


if __name__ == "__main__":
    main()
