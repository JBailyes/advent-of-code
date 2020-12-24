import re

from aocutils import load_input


def main():
    puzzle_input = load_input(__file__)
    # puzzle_input = load_input(__file__, 'example')

    WHITE = True
    BLACK = False

    def decode_coord(vectors_string):
        nw = vectors_string.count('nw')
        sw = vectors_string.count('sw')
        ne = vectors_string.count('ne')
        se = vectors_string.count('se')
        ew_string = re.sub(r'[ns][ew]', '', vectors_string)
        e = ew_string.count('e')
        w = ew_string.count('w')
        return ne + se + e * 2 - nw - sw - w * 2, ne + nw - se - sw

    tiles = {}
    for line in puzzle_input:
        tile = decode_coord(line)
        if tile not in tiles:
            tiles[tile] = WHITE
        tiles[tile] = not tiles[tile]

    def get_tile(coord, arrangement) -> bool:
        if coord in arrangement:
            return arrangement[coord]
        return WHITE

    def get_adjacent_coords(coord):
        x, y = coord
        #                    e       w        ne      nw       se       sw
        adjacent_vectors = [(2, 0), (-2, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]
        return [(x + long, y + lat) for long, lat in adjacent_vectors]

    prev_state = tiles.copy()
    for day in range(100):

        for coord in [coord for coord, state in prev_state.items() if state is BLACK]:
            for adjacent_coord in get_adjacent_coords(coord):
                if adjacent_coord not in prev_state:
                    prev_state[adjacent_coord] = WHITE
        new_state = prev_state.copy()

        for coord in new_state:
            adjacent_states = [get_tile(adjacent, prev_state) for adjacent in get_adjacent_coords(coord)]
            adjacent_black = adjacent_states.count(BLACK)

            if prev_state[coord] == BLACK:
                if adjacent_black == 0 or adjacent_black > 2:
                    new_state[coord] = WHITE
            elif adjacent_black == 2:
                new_state[coord] = BLACK

        prev_state = new_state

        blacks = list(new_state.values()).count(BLACK)
        print('Day', day + 1, ': ', blacks)


if __name__ == "__main__":
    main()
