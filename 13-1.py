import argparse
import re
import string
from datetime import datetime
import operator
import sys
import colorama
from colorama import Fore,  Back,  Style
from os.path import basename
import math

from computer import Computer


def parse(code_line):
    programme = []
    for code in code_line.split(","):
        programme.append(int(code))
    return programme


class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return str(self.x) + ',' + str(self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(str(self.x) + ',' + str(self.y))


class Grid:
    def __init__(self):
        self._tiles: dict = {Coord(0, 0): 0}
        self._min_x = 0
        self._max_x = 0
        self._min_y = 0
        self._max_y = 0

    def get_tile(self, coord: Coord):
        if coord not in self._tiles.keys():
            return 0
        return self._tiles[coord]

    def set_tile(self, x, y, tile_id):
        coord = Coord(x, y)
        self._tiles[coord] = tile_id
        self._min_x = min(coord.x, self._min_x)
        self._max_x = max(coord.x, self._max_x)
        self._min_y = min(coord.y, self._min_y)
        self._max_y = max(coord.y, self._max_y)

    def count_type(self, tile_type):
        count = 0
        for tile in self._tiles.values():
            if tile == tile_type:
                count += 1
        return count

    def __str__(self):
        image = ''
        for y in range(self._min_y, self._max_y + 1):
            for x in range(self._min_x, self._max_x + 1):
                coord = Coord(x, y)
                tile_id = 0
                if coord in self._tiles.keys():
                    tile_id = self._tiles[coord]
                if tile_id == 0:
                    image += ' '
                else:
                    image += str(tile_id)
            image += '\n'
        return image

    def __repr__(self):
        return self.__str__()


class Game:
    def __init__(self, programme, grid):
        self._programme = programme.copy()
        self._computer = Computer(programme, [], debug=False)
        self._grid: Grid = grid

    def play(self):
        while self._computer.state() != 'halt':
            self._computer.run()
            while len(self._computer.outputs()) > 0:
                x = self._computer.read()
                y = self._computer.read()
                tile_id = self._computer.read()
                self._grid.set_tile(x, y, tile_id)


def main():
    colorama.init()

    inputFile = basename(__file__)[:2] + '-input.txt'
    lines = []
    with open(inputFile,  'r') as infile:
        for line in infile:
            lines.append(line.strip())

    programme = parse(lines[0])

    grid = Grid()
    game = Game(programme, grid)
    game.play()

    print(grid)
    print('')
    print(grid.count_type(2))



if __name__ == "__main__":
    main()
