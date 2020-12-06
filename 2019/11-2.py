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


class Computer:
    def __init__(self, programme, inputs):
        self._memory = {}
        self._inputs = inputs
        self._outputs = []
        self._instruction_pointer = 0
        self._relative_base = 0
        self._state = 'init'

        for address in range(0, len(programme)):
            self._write(address, programme[address])

    def input(self, value):
        self._inputs.append(value)

    def outputs(self):
        return self._outputs

    def state(self):
        return self._state

    def run(self):
        # programme = self._programme
        self._state = 'run'
        while self._state != 'halt':
            instruction = '{0:05}'.format(self._read(self._instruction_pointer))
            opcode = int(instruction[-2:])
            param_1_mode = int(instruction[2])
            param_2_mode = int(instruction[1])
            param_3_mode = int(instruction[0])
            # print(instruction)
            # print('{0}: op {1} p1m {2} p2m {3} p3m {4}'.format(
            #     instruction, opcode, param_1_mode, param_2_mode, param_3_mode))
            if opcode == 1:
                # addition
                param_1 = self._read(self._instruction_pointer + 1)
                value_1 = self._get_value(param_1, param_1_mode)
                param_2 = self._read(self._instruction_pointer + 2)
                value_2 = self._get_value(param_2, param_2_mode)
                param_3 = self._read(self._instruction_pointer + 3)
                self._write(param_3, value_1 + value_2, param_3_mode)
                self._instruction_pointer += 4
            elif opcode == 2:
                # multiplicaiton
                param_1 = self._read(self._instruction_pointer + 1)
                value_1 = self._get_value(param_1, param_1_mode)
                param_2 = self._read(self._instruction_pointer + 2)
                value_2 = self._get_value(param_2, param_2_mode)
                param_3 = self._read(self._instruction_pointer + 3)
                self._write(param_3, value_1 * value_2, param_3_mode)
                self._instruction_pointer += 4
            elif opcode == 3:
                # input
                if len(self._inputs) == 0:
                    self._state = 'wait'
                    return
                input_value = self._inputs.pop(0)
                store_address = self._read(self._instruction_pointer + 1)
                # print('  Store {0} at {1}, mode {2}'.format(input_value, store_address, param_1_mode))
                self._write(store_address, input_value, param_1_mode)
                self._instruction_pointer += 2
            elif opcode == 4:
                # output
                param_1 = self._read(self._instruction_pointer + 1)
                value_1 = self._get_value(param_1, param_1_mode)
                # print('  Output: read {0} from {1}'.format(value_1, param_1))
                self._outputs.append(value_1)
                self._instruction_pointer += 2
            elif opcode == 5:
                # jump if true
                param_1 = self._read(self._instruction_pointer + 1)
                value_1 = self._get_value(param_1, param_1_mode)
                param_2 = self._read(self._instruction_pointer + 2)
                value_2 = self._get_value(param_2, param_2_mode)
                if value_1 != 0:
                    self._instruction_pointer = value_2
                else:
                    self._instruction_pointer += 3
            elif opcode == 6:
                # jump if false
                param_1 = self._read(self._instruction_pointer + 1)
                value_1 = self._get_value(param_1, param_1_mode)
                param_2 = self._read(self._instruction_pointer + 2)
                value_2 = self._get_value(param_2, param_2_mode)
                if value_1 == 0:
                    self._instruction_pointer = value_2
                else:
                    self._instruction_pointer += 3
            elif opcode == 7:
                # less than
                param_1 = self._read(self._instruction_pointer + 1)
                value_1 = self._get_value(param_1, param_1_mode)
                param_2 = self._read(self._instruction_pointer + 2)
                value_2 = self._get_value(param_2, param_2_mode)
                param_3 = self._read(self._instruction_pointer + 3)
                if value_1 < value_2:
                    self._write(param_3, 1, param_3_mode)
                else:
                    self._write(param_3, 0, param_3_mode)
                self._instruction_pointer += 4
            elif opcode == 8:
                # equals
                param_1 = self._read(self._instruction_pointer + 1)
                value_1 = self._get_value(param_1, param_1_mode)
                param_2 = self._read(self._instruction_pointer + 2)
                value_2 = self._get_value(param_2, param_2_mode)
                param_3 = self._read(self._instruction_pointer + 3)
                if value_1 == value_2:
                    self._write(param_3, 1, param_3_mode)
                else:
                    self._write(param_3, 0, param_3_mode)
                self._instruction_pointer += 4
            elif opcode == 9:
                # equals
                param_1 = self._read(self._instruction_pointer + 1)
                value_1 = self._get_value(param_1, param_1_mode)
                self._relative_base += value_1
                self._instruction_pointer += 2
            elif opcode == 99:
                self._state = 'halt'
                return

    def _get_value(self, param, param_mode):
        if param_mode == 0:
            return self._read(param)
        elif param_mode == 1:
            return param
        elif param_mode == 2:
            return self._read(param + self._relative_base)

    def _read(self, address):
        if address not in self._memory.keys():
            self._write(address, 0)
        return self._memory[address]

    def _write(self, address, value, mode=1):
        if mode == 2:
            self._memory[address + self._relative_base] = value
        else:
            self._memory[address] = value


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


class Hull:
    def __init__(self):
        self._panels: dict = {Coord(0, 0): 0}
        self._painted_panels = set()
        self._min_x = 0
        self._max_x = 0
        self._min_y = 0
        self._max_y = 0

    def get(self, coord:Coord):
        if coord not in self._panels.keys():
            return 0
        return self._panels[coord]

    def paint(self, coord: Coord, colour):
        self._panels[coord] = colour
        self._painted_panels.add(coord)
        self._min_x = min(coord.x, self._min_x)
        self._max_x = max(coord.x, self._max_x)
        self._min_y = min(coord.y, self._min_y)
        self._max_y = max(coord.y, self._max_y)

    def __str__(self):
        image = ''
        for y in range(self._min_y, self._max_y + 1):
            for x in range(self._min_x, self._max_x + 1):
                coord = Coord(x, y)
                colour = 0
                if coord in self._panels.keys():
                    colour = self._panels[coord]
                if colour == 0:
                    image += '.'
                else:
                    image += '#'
            image += '\n'
        return image

    def __repr__(self):
        return self.__str__()


class Robot:
    def __init__(self, programme, hull):
        self._programme = programme.copy()
        self._computer = Computer(programme, [])
        self._pos = Coord(0, 0)
        self._direction = '^'
        self._hull: Hull = hull

    def paint(self):
        while self._computer.state() != 'halt':
            current_panel = self._hull.get(self._pos)
            print('current panel {0} colour {1}'.format(self._pos, current_panel))
            self._computer.input(current_panel)
            self._computer.run()
            print('   outputs:', self._computer.outputs())
            new_colour = self._computer.outputs().pop(0)
            new_direction = self._computer.outputs().pop(0)

            self._hull.paint(self._pos, new_colour)
            self.move(new_direction)

    def move(self, new_direction):
        compass = ['<', '^', '>', 'v']
        if new_direction == 0:
            compass_change = -1
        else:
            compass_change = 1
        current_compass_index = compass.index(self._direction)
        self._direction = compass[(current_compass_index + compass_change) % 4]
        print('   new direction:', self._direction)
        vector_map = {
            '>': [1, 0],
            '<': [-1, 0],
            '^': [0, -1],
            'v': [0, 1],
        }
        self._pos = Coord(self._pos.x + vector_map[self._direction][0],
                          self._pos.y + vector_map[self._direction][1])
        print('   new pos:', self._pos)


def main():
    colorama.init()

    inputFile = basename(__file__)[:2] + '-input.txt'
    lines = []
    with open(inputFile,  'r') as infile:
        for line in infile:
            lines.append(line.strip())

    programme = parse(lines[0])

    hull = Hull()
    hull._panels[Coord(0, 0)] = 1
    robot = Robot(programme, hull)
    robot.paint()

    print('painted panels:', len(hull._painted_panels))

    print(hull)

if __name__ == "__main__":
    main()
