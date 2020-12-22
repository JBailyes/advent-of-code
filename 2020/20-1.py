from aocutils import load_input

import re


class Tile:
    def __init__(self, tile_id, lines):
        self.tile_id: int = tile_id
        self.lines = lines

        edges = [lines[0]]  # top
        left = ''
        right = ''
        for line in lines:
            left += line[0]
            right += line[-1]
        edges.append(right)
        edges.append(lines[-1])  # bottom
        edges.append(left)

        self.edges = edges

    def __hash__(self):
        return self.tile_id


def main():
    puzzle_input = load_input(__file__)
    puzzle_input = load_input(__file__, 'example')

    puzzle_input.append('')
    tiles = []

    all_input = '\n'.join(puzzle_input)
    for tile_match in re.finditer(r'Tile (\d+):\n([.#\n]*[^\n])\n', all_input):
        print('Tile', tile_match.group(1), ':')
        tile = Tile(int(tile_match.group(1)), tile_match.group(2).split('\n'))
        tiles.append(tile)

    for y in [0 1 2]:
        for x in [0 1 2]:
            pass


if __name__ == "__main__":
    main()
