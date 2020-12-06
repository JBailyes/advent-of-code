import argparse
import re
import string
from datetime import datetime
import operator
import sys
import colorama
from colorama import Fore, Back, Style
from os.path import basename
import math
from itertools import permutations


class Amp:
    def __init__(self, programme, phase_setting):
        self.__programme = programme
        self.__inputs = [phase_setting]
        self.__outputs = []
        self.__instruction_pointer = 0
        self.__state = 'init'

    def input(self, value):
        self.__inputs.append(value)

    def outputs(self):
        return self.__outputs

    def state(self):
        return self.__state

    def run(self):
        programme = self.__programme
        self.__state = 'run'
        while self.__instruction_pointer < len(programme):
            instruction = '{0:05}'.format(programme[self.__instruction_pointer])
            opcode = int(instruction[-2:])
            param_1_mode = int(instruction[2])
            param_2_mode = int(instruction[1])
            param_3_mode = int(instruction[0])
            # print('{0}: op {1} p1m {2} p2m {3} p3m {4}'.format(
            #     instruction, opcode, param_1_mode, param_2_mode, param_3_mode))
            if opcode == 1:
                # addition
                param_1 = programme[self.__instruction_pointer + 1]
                value_1 = get_value(programme, param_1, param_1_mode)
                param_2 = programme[self.__instruction_pointer + 2]
                value_2 = get_value(programme, param_2, param_2_mode)
                param_3 = programme[self.__instruction_pointer + 3]
                programme[param_3] = value_1 + value_2
                self.__instruction_pointer += 4
            elif opcode == 2:
                # multiplicaiton
                param_1 = programme[self.__instruction_pointer + 1]
                value_1 = get_value(programme, param_1, param_1_mode)
                param_2 = programme[self.__instruction_pointer + 2]
                value_2 = get_value(programme, param_2, param_2_mode)
                param_3 = programme[self.__instruction_pointer + 3]
                programme[param_3] = value_1 * value_2
                self.__instruction_pointer += 4
            elif opcode == 3:
                # input
                if len(self.__inputs) == 0:
                    self.__state = 'wait'
                    return
                input_value = self.__inputs.pop(0)
                store_address = programme[self.__instruction_pointer + 1]
                # print('  Store {0} at {1}'.format(input_value, store_address))
                programme[store_address] = input_value
                self.__instruction_pointer += 2
            elif opcode == 4:
                # output
                param_1 = programme[self.__instruction_pointer + 1]
                value_1 = get_value(programme, param_1, param_1_mode)
                # print('  Output: read {0} from {1}'.format(value_1, param_1))
                self.__outputs.append(value_1)
                self.__instruction_pointer += 2
            elif opcode == 5:
                # jump if true
                param_1 = programme[self.__instruction_pointer + 1]
                value_1 = get_value(programme, param_1, param_1_mode)
                param_2 = programme[self.__instruction_pointer + 2]
                value_2 = get_value(programme, param_2, param_2_mode)
                if value_1 != 0:
                    self.__instruction_pointer = value_2
                else:
                    self.__instruction_pointer += 3
            elif opcode == 6:
                # jump if false
                param_1 = programme[self.__instruction_pointer + 1]
                value_1 = get_value(programme, param_1, param_1_mode)
                param_2 = programme[self.__instruction_pointer + 2]
                value_2 = get_value(programme, param_2, param_2_mode)
                if value_1 == 0:
                    self.__instruction_pointer = value_2
                else:
                    self.__instruction_pointer += 3
            elif opcode == 7:
                # less than
                param_1 = programme[self.__instruction_pointer + 1]
                value_1 = get_value(programme, param_1, param_1_mode)
                param_2 = programme[self.__instruction_pointer + 2]
                value_2 = get_value(programme, param_2, param_2_mode)
                param_3 = programme[self.__instruction_pointer + 3]
                if value_1 < value_2:
                    programme[param_3] = 1
                else:
                    programme[param_3] = 0
                self.__instruction_pointer += 4
            elif opcode == 8:
                # equals
                param_1 = programme[self.__instruction_pointer + 1]
                value_1 = get_value(programme, param_1, param_1_mode)
                param_2 = programme[self.__instruction_pointer + 2]
                value_2 = get_value(programme, param_2, param_2_mode)
                param_3 = programme[self.__instruction_pointer + 3]
                if value_1 == value_2:
                    programme[param_3] = 1
                else:
                    programme[param_3] = 0
                self.__instruction_pointer += 4
            elif opcode == 99:
                self.__state = 'halt'
                return


def get_value(programme, param, param_mode):
    if param_mode == 0:
        return programme[param]
    elif param_mode == 1:
        return param


def thruster_signal(programme, phase_settings):
    amps = []
    for phase_setting in phase_settings:
        amps.append(Amp(programme.copy(), phase_setting))

    last_output = 0
    while amps[0].state() != 'halt':
        for amp in amps:
            amp.input(last_output)
            amp.run()
            last_output = amp.outputs()[-1]

    return last_output


def parse(code_line):
    programme = []
    for code in code_line.split(","):
        programme.append(int(code))
    return programme


def main():
    colorama.init()

    inputFile = basename(__file__)[:2] + '-input.txt'
    code_line = ''
    with open(inputFile, 'r') as infile:
        for line in infile:
            code_line = line.strip()

    # code_line = '3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5'
    # code_line = '3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0'
    programme = parse(code_line)

    # print(thruster_signal(programme, [4,3,2,1,0]))
    # print(thruster_signal(programme, [0,1,2,3,4]))

    highest_signal = 0
    best_phase_sequence = []
    for phase_sequence in permutations([5, 6, 7, 8, 9]):
        signal = thruster_signal(programme, phase_sequence)
        if signal > highest_signal:
            best_phase_sequence = phase_sequence
            highest_signal = signal

    print(highest_signal, "from", best_phase_sequence)


if __name__ == "__main__":
    main()
