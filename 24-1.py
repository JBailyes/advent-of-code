import string
from os.path import basename
from typing import Dict, List, Set

import colorama
from colorama import Fore, Back


class XY:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return str(self.x) + ',' + str(self.y)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(str(self.x) + ',' + str(self.y))

    def up(self):
        return self.relative_location(1)

    def down(self):
        return self.relative_location(2)

    def left(self):
        return self.relative_location(3)

    def right(self):
        return self.relative_location(4)

    def relative_location(self, direction: int):
        offset = {
            1: XY(0, -1),
            2: XY(0, 1),
            3: XY(-1, 0),
            4: XY(1, 0)
        }[direction]
        return XY(self.x + offset.x, self.y + offset.y)


class Tile:
    def __init__(self, pos: XY, value):
        self.pos = pos
        self.value = value
        self.bio_number = 2 ** (pos.y * 5 + pos.x)


class Eris:

    def __init__(self):
        self.tiles: Dict[XY, Tile] = {}
        self.min_x = None
        self.max_x = None
        self.min_y = None
        self.max_y = None

    def tile_locations(self):
        return self.tiles.keys()

    def get(self, coord: XY) -> str:
        if coord not in self.tiles.keys():
            return '.'
        return self.tiles[coord].value

    def set(self, pos: XY, value: str):
        if pos not in self.tiles.keys():
            self.tiles[pos] = Tile(pos, value)
        else:
            self.tiles[pos].value = value
        if self.min_x is None:
            self.min_x = pos.x
        else:
            self.min_x = min(pos.x, self.min_x)

        if self.max_x is None:
            self.max_x = pos.x
        else:
            self.max_x = max(pos.x, self.max_x)

        if self.min_y is None:
            self.min_y = pos.y
        else:
            self.min_y = min(pos.y, self.min_y)

        if self.max_y is None:
            self.max_y = pos.y
        else:
            self.max_y = max(pos.y, self.max_y)

    def draw(self):
        for y in range(self.min_y, self.max_y + 1):
            for x in range(self.min_x, self.max_x + 1):
                coord = XY(x, y)
                value = self.get(coord)
                print(value, end='')
                print(Fore.RESET + Back.RESET, end='')
            print('')
        print('\n\n')

    def __str__(self):
        image = ''
        for y in range(self.min_y, self.max_y + 1):
            for x in range(self.min_x, self.max_x + 1):
                coord = XY(x, y)
                if coord in self.tiles.keys():
                    value = self.tiles[coord].value
                    image += str(value)

            image += '\n'
        return image

    def __repr__(self):
        return self.__str__()

    def bio_rating(self):
        rating = 0
        for pos, tile in self.tiles.items():
            if tile.value == '#':
                rating += tile.bio_number
        return rating

    def one_minute(self):
        to_infest: List[XY] = []
        to_clear: List[XY] = []
        for pos, tile in self.tiles.items():
            adjacent_bugs = 0
            for adj in [pos.up(), pos.down(), pos.left(), pos.right()]:
                if self.get(adj) == '#':
                    adjacent_bugs += 1
            if tile.value == '#' and adjacent_bugs != 1:
                to_clear.append(pos)
            elif tile.value == '.' and adjacent_bugs in [1, 2]:
                to_infest.append(pos)
        for pos in to_infest:
            self.set(pos, '#')
        for pos in to_clear:
            self.set(pos, '.')


def main():
    colorama.init()

    eris = Eris()

    inputFile = basename(__file__)[:2] + '-input.txt'
    # inputFile = basename(__file__)[:2] + '-example-1.txt'

    y = 0
    with open(inputFile,  'r') as infile:
        for line in infile:
            for x, val in enumerate(line.rstrip()):
                pos = XY(x, y)
                eris.set(pos, val)
            y += 1

    eris.draw()

    prev_bio_ratings = []
    bio_rating = eris.bio_rating()
    while bio_rating not in prev_bio_ratings:
        prev_bio_ratings.append(bio_rating)
        eris.one_minute()
        bio_rating = eris.bio_rating()

    eris.draw()
    print(bio_rating)


if __name__ == "__main__":
    main()
