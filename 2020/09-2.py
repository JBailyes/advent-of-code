import argparse


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('target')
    args = parser.parse_args()

    lines = []
    with open(args.input, 'r') as infile:
        for line in infile:
            lines.append(line.strip())

    numbers = []
    for line in lines:
        numbers.append(int(line))
    target = int(args.target)

    for i in range(0, len(numbers)):
        sum = 0
        constituents = []
        j = i
        while j < len(numbers) and sum < target:
            current_number = numbers[j]
            constituents.append(current_number)
            sum += current_number
            j += 1
        if sum == target:
            smallest = min(constituents)
            largest = max(constituents)
            print(constituents)
            print('{} + {} = {}'.format(smallest, largest, smallest + largest))
            break


if __name__ == "__main__":
    main()
