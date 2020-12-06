import argparse


def main():
    # Load the sequence
    parser = argparse.ArgumentParser()
    parser.add_argument('infile')
    args = parser.parse_args()

    boxids = []
    with open(args.infile) as infile:
        for line in infile:
            boxid = line.strip()
            boxids.append(boxid)

    twos = 0
    threes = 0

    for boxid in boxids:
        print(boxid)
        letterCounts = {}
        for letter in boxid:
            if letter not in letterCounts:
                letterCounts[letter] = 1
            else:
                letterCounts[letter] += 1
        hasTwos = False
        hasThrees = False
        for (letter, letterCount) in letterCounts.items():
            if letterCount == 2:
                hasTwos = True
                print('   2 {0}'.format(letter))
            elif letterCount == 3:
                hasThrees = True
                print('   3 {0}'.format(letter))
        if hasTwos:
            twos += 1
        if hasThrees:
            threes += 1

    checksum = twos * threes
    print('Checksum: {0}'.format(checksum))

    print('Finish')


if __name__ == "__main__":
    main()
