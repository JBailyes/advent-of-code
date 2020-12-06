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

    found = False
    for i in range(len(boxids)):
        if found:
            break
        for j in range(i + 1, len(boxids)):
            if found:
                break
            box1 = boxids[i]
            box2 = boxids[j]
            diffs = []
            common = set()
            for k in range(len(box1)):
                letter1 = box1[k]
                letter2 = box2[k]
                if letter1 != letter2:
                    diffs.append(k)
                else:
                    common.add(letter1)
            if len(diffs) == 1:
                diffpos = diffs[0]
                print(box1)
                print(box2)
                print('  Diff at pos {0}, letters {1} and {2}'.format(diffs[0], box1[diffs[0]], box2[diffs[0]]))
                print('  Common letters: {0}'.format(''.join(sorted(common))))
                print('  {0}'.format(box1[0:diffpos] + box1[diffpos+1:]))
                found = True

    print('Finish')


if __name__ == "__main__":
    main()
