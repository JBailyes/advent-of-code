import re

from aocutils import load_input


def main():
    puzzle_input = load_input(__file__)
    # puzzle_input = load_input(__file__, 'example')

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
            tiles[tile] = False
        tiles[tile] = not tiles[tile]

    flipped = len([tile for tile in tiles.values() if tile])
    print(flipped)


if __name__ == "__main__":
    main()
