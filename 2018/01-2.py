import argparse


def main():
    # Load the sequence
    parser = argparse.ArgumentParser()
    parser.add_argument('infile')
    args = parser.parse_args()

    sequence = []
    with open(args.infile) as infile:
        for line in infile:
            number = int(line.strip())
            sequence.append(number)

    frequency = 0
    for number in sequence:
        frequency += number
    print('Frequency after 1 run: {0}'.format(frequency))

    frequencies = set()
    frequencies.add(0)
    frequency = 0
    repeated = False
    while not repeated:
        for number in sequence:
            frequency += number
            if frequency in frequencies:
                print('First repeat frequency: {0}'.format(frequency))
                repeated = True
                break
            else:
                frequencies.add(frequency)

    print('Finish')


if __name__ == "__main__":
    main()
