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

    def scenic_score(tree: int, trees_left: list[int], trees_right: list[int], trees_up: list[int], trees_down: list[int]):
        def get_view(tree: int, other_trees: list[int]) -> int:
            distance = 0
            for distance, other_tree in enumerate(other_trees, start=1):
                if other_tree >= tree:
                    return distance
            return distance

        return get_view(tree, reversed(trees_left)) * get_view(tree, trees_right) * \
                    get_view(tree, reversed(trees_up)) * get_view(tree, trees_down)   


    most_scenic = 0

    for x in range(width):
        for y in range(height):
            tree = xy_grid[x][y]
            trees_left = yx_grid[y][0:x]
            trees_right = yx_grid[y][x + 1:]
            trees_up = xy_grid[x][0:y]
            trees_down = xy_grid[x][y + 1:]

            most_scenic = max(most_scenic,
                            scenic_score(tree, trees_left, trees_right, trees_up, trees_down))


    print(most_scenic)
    # Correct answer: 263670


if __name__ == "__main__":
    main()
