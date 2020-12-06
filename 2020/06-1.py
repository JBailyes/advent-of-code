import argparse


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()

    lines = []
    with open(args.input, 'r') as infile:
        for line in infile:
            lines.append(line.strip())
    if lines[-1] != '':
        lines.append('')

    yes_counts = []
    group_yesses = set()
    for line in lines:
        if line == '':
            yes_counts.append(len(group_yesses))
            group_yesses = set()
        else:
            for letter in line:
                group_yesses.add(letter)

    print('Group yesses:', yes_counts, sum(yes_counts))
    print('Sum:', sum(yes_counts))


if __name__ == "__main__":
    main()
