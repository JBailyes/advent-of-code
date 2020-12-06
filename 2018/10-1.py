import argparse
import re
import string
import time


class Star:
    def __init__(self, sx, sy, vx, vy):
        self.startX = sx
        self.startY = sy
        self.vx = vx
        self.vy = vy

    def __str__(self):
        return '{' + '"px": {0:3}, "py": {1:3}, "vx": {2:3}, "vy": {3:3}'.format(
            self.startX, self.startY, self.vx, self.vy) + '},'


def main():
    # Load the sequence
    parser = argparse.ArgumentParser()
    parser.add_argument('infile')
    args = parser.parse_args()

    stars = []

    maxX = 0
    minX = 0
    maxY = 0
    minY = 0

    with open(args.infile) as infile:
        for line in infile:
            match = re.search(r'(-?\d+), +(-?\d+)[^\d-]+(-?\d), +(-?\d+)', line.strip())
            px = int(match.group(1))
            py = int(match.group(2))
            vx = int(match.group(3))
            vy = int(match.group(4))
            stars.append(Star(px, py, vx, vy))
            minX = min(minX, px)
            maxX = max(maxX, px)
            minY = min(minY, py)
            maxY = max(maxY, py)

    for star in stars:
        print(star)

    print('X range {0} to {1}'.format(minX, maxX))
    print('Y range {0} to {1}'.format(minY, maxY))


    print()
    print('Finish')


if __name__ == "__main__":
    main()
