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

    tree_counts = []
    product = 1

    for slope_right, slope_down in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]:
        tree_count = 0
        x = 0
        for row_num in range(0, len(grid), slope_down):
            geology = grid[row_num][x % width]
            if geology == '#':
                tree_count += 1
            x += slope_right
        tree_counts.append(tree_count)
        product *= tree_count

    print('trees:', tree_counts)
    print('product:', product)


if __name__ == "__main__":
    main()
