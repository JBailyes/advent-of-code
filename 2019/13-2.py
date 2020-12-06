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
import time
from computer import Computer
import msvcrt


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
        self._ball_pos = Coord(0, 0)
        self._paddle_pos = Coord(0, 0)

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
        if tile_id == 3:
            self._paddle_pos = coord
        elif tile_id == 4:
            self._ball_pos = coord

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
                elif tile_id == 2:
                    image += '#'
                elif tile_id == 3:
                    image += '-'
                elif tile_id == 4:
                    image += 'o'
                else:
                    image += str(tile_id)

            image += '\n'
        return image

    def __repr__(self):
        return self.__str__()


class Game:
    def __init__(self, programme, grid, save_file_name):
        self._programme = programme.copy()

        # save_data = []
        # with open(save_file_name, 'r') as save_file:
        #     for line in save_file:
        #         save_data = parse(line.strip())

        start_inputs = []
        # for num in save_data:
        #     start_inputs.append(num)

        self._computer = Computer(programme, start_inputs, debug=False)
        self._grid: Grid = grid
        self._score = 0
        # self._save_file = save_file_name
        # self._moves = start_inputs.copy()

    def score(self):
        return self._score

    # def save(self):
    #     moves_as_str = []
    #     for move in self._moves:
    #         moves_as_str.append(str(move))
    #     with open(self._save_file, 'w') as save_file:
    #         save_file.write(','.join(moves_as_str))

    def play(self):
        while self._computer.state() != 'halt':
            self._computer.run()

            if self._computer.state() == 'wait':
                # print(self._grid)
                # print('')
                # print("Joystick [left 1, neutral 2, right 3]: ")
                # key = str(msvcrt.getch(), encoding='utf-8')
                # if key == 's':
                #     self.save()
                #     key = str(msvcrt.getch(), encoding='utf-8')
                # direction = int(key) - 2
                direction = 0
                if self._grid._paddle_pos.x > self._grid._ball_pos.x:
                    direction = -1
                elif self._grid._paddle_pos.x < self._grid._ball_pos.x:
                    direction = 1
                # self._moves.append(direction)
                self._computer.input(direction)
                # time.sleep(0.025)
                self._computer.run()

            while len(self._computer.outputs()) > 0:
                x = self._computer.read()
                y = self._computer.read()
                if x == -1 and y == 0:
                    self._score = self._computer.read()
                else:
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
    programme[0] = 2

    saveFile = basename(__file__)[:2] + '.save.txt'

    grid = Grid()
    game = Game(programme, grid, saveFile)
    game.play()

    print(grid)
    print('')
    print('Score:', game.score())


if __name__ == "__main__":
    main()
