import argparse


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()

    grid = []

    with open(args.input, 'r') as infile:
        for line in infile:
            new_line = []
            for coord in line.strip():
                new_line.append(coord)
            grid.append(new_line)

    width = len(grid[0])

    tree_count = 0
    x = 0
    for row in grid:
        geology = row[x % width]
        if geology == '#':
            tree_count += 1
        x += 3

    print('trees:', tree_count)

if __name__ == "__main__":
    main()
