from aocutils import load_input


def main():
    puzzle_input = load_input(__file__)
    # puzzle_input = load_input(__file__, 'example')

    yx_grid = []

    for y,line in enumerate(puzzle_input):
        row = []
        yx_grid.append(row)
        for x,tree_height_str in enumerate(line):
            row.append(int(tree_height_str))

    width = len(yx_grid[0])
    height = len(yx_grid)

    xy_grid = []
    for x in range(width):
        xy_grid.append([])
        for y in range(height):
            xy_grid[x].append(yx_grid[y][x])
    
    width = len(yx_grid[0])
    height = len(yx_grid)
    visible = width * 2 + height * 2 - 4  # outer edge

    for x in range(1, width - 1):
        for y in range(1, height - 1):
            tree = xy_grid[x][y]
            vis_left = max(yx_grid[y][0:x]) < tree
            vis_right = max(yx_grid[y][x + 1:]) < tree
            vis_top = max(xy_grid[x][0:y]) < tree
            vis_bottom = max(xy_grid[x][y + 1:]) < tree

            if True in [vis_left, vis_right, vis_top, vis_bottom]:
                visible += 1

    print(visible)
    # Correct answer: 1835


if __name__ == "__main__":
    main()
