import argparse
import re

def main():
    # Load the sequence
    parser = argparse.ArgumentParser()
    parser.add_argument('infile')
    args = parser.parse_args()

    claims = []
    with open(args.infile) as infile:
        for line in infile:
            claims.append(line.strip())

    # claims = [
    #     '#1 @ 1,3: 4x4',
    #     '#2 @ 3,1: 4x4',
    #     '#3 @ 5,5: 2x2'
    # ]

    allClaimIds = set()
    inchClaims = {}

    for claim in claims:
        # print(claim)
        match = re.search(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)', claim)
        if match:
            claimId = match.group(1)
            left = int(match.group(2))
            top = int(match.group(3))
            width = int(match.group(4))
            height = int(match.group(5))
            allClaimIds.add(claimId)

            for y in range(top, top + height):
                for x in range(left, left + width):
                    inchCoordinate = '{0},{1}'.format(x, y)
                    # print('   ' + inchCoordinate)
                    if inchCoordinate not in inchClaims.keys():
                        inchClaims[inchCoordinate] = []
                    inchClaims[inchCoordinate].append(claimId)

    clearClaimIds = set(allClaimIds)
    duplicateClaims = 0
    for coords,ids in inchClaims.items():
        # print(coords + ': ' + str(ids))
        if len(ids) > 1:
            duplicateClaims += 1
            clearClaimIds -= set(ids)

    print('{0} square inches have overlapping claims'.format(duplicateClaims))

    print('{0} claim IDs have no overlaps'.format(clearClaimIds))

    print('Finish')


if __name__ == "__main__":
    main()
