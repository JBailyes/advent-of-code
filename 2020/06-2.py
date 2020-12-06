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
    group_yesses = []
    for line in lines:
        if line == '':
            all_yes = group_yesses[0]
            for yesses in group_yesses[1:]:
                all_yes &= yesses
            yes_counts.append(len(all_yes))
            group_yesses = []
        else:
            group_yesses.append(set(line))

    print('Group yesses:', yes_counts, sum(yes_counts))
    print('Sum:', sum(yes_counts))


if __name__ == "__main__":
    main()
