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

def run(programme, inputs):
    outputs = []
    instruction_pointer = 0
    while instruction_pointer < len(programme):
        instruction = '{0:05}'.format(programme[instruction_pointer])
        opcode = int(instruction[-2:])
        param_1_mode = int(instruction[2])
        param_2_mode = int(instruction[1])
        param_3_mode = int(instruction[0])
        # print('{0}: op {1} p1m {2} p2m {3} p3m {4}'.format(
        #     instruction, opcode, param_1_mode, param_2_mode, param_3_mode))
        if opcode == 1:
            # addition
            param_1 = programme[instruction_pointer + 1]
            value_1 = get_value(programme, param_1, param_1_mode)
            param_2 = programme[instruction_pointer + 2]
            value_2 = get_value(programme, param_2, param_2_mode)
            param_3 = programme[instruction_pointer + 3]
            programme[param_3] = value_1 + value_2
            instruction_pointer += 4
        elif opcode == 2:
            # multiplicaiton
            param_1 = programme[instruction_pointer + 1]
            value_1 = get_value(programme, param_1, param_1_mode)
            param_2 = programme[instruction_pointer + 2]
            value_2 = get_value(programme, param_2, param_2_mode)
            param_3 = programme[instruction_pointer + 3]
            programme[param_3] = value_1 * value_2
            instruction_pointer += 4
        elif opcode == 3:
            # input
            input_value = inputs.pop(0)
            store_address = programme[instruction_pointer + 1]
            # print('  Store {0} at {1}'.format(input_value, store_address))
            programme[store_address] = input_value
            instruction_pointer += 2
        elif opcode == 4:
            # output
            param_1 = programme[instruction_pointer + 1]
            value_1 = get_value(programme, param_1, param_1_mode)
            # print('  Output: read {0} from {1}'.format(value_1, param_1))
            outputs.append(value_1)
            instruction_pointer += 2
        elif opcode == 5:
            # jump if true
            param_1 = programme[instruction_pointer + 1]
            value_1 = get_value(programme, param_1, param_1_mode)
            param_2 = programme[instruction_pointer + 2]
            value_2 = get_value(programme, param_2, param_2_mode)
            if value_1 != 0:
                instruction_pointer = value_2
            else:
                instruction_pointer += 3
        elif opcode == 6:
            # jump if false
            param_1 = programme[instruction_pointer + 1]
            value_1 = get_value(programme, param_1, param_1_mode)
            param_2 = programme[instruction_pointer + 2]
            value_2 = get_value(programme, param_2, param_2_mode)
            if value_1 == 0:
                instruction_pointer = value_2
            else:
                instruction_pointer += 3
        elif opcode == 7:
            # less than
            param_1 = programme[instruction_pointer + 1]
            value_1 = get_value(programme, param_1, param_1_mode)
            param_2 = programme[instruction_pointer + 2]
            value_2 = get_value(programme, param_2, param_2_mode)
            param_3 = programme[instruction_pointer + 3]
            if value_1 < value_2:
                programme[param_3] = 1
            else:
                programme[param_3] = 0
            instruction_pointer += 4
        elif opcode == 8:
            # equals
            param_1 = programme[instruction_pointer + 1]
            value_1 = get_value(programme, param_1, param_1_mode)
            param_2 = programme[instruction_pointer + 2]
            value_2 = get_value(programme, param_2, param_2_mode)
            param_3 = programme[instruction_pointer + 3]
            if value_1 == value_2:
                programme[param_3] = 1
            else:
                programme[param_3] = 0
            instruction_pointer += 4
        elif opcode == 99:
            # instruction_pointer += 1
            return outputs
    return outputs


def get_value(programme, param, param_mode):
    if param_mode == 0:
        return programme[param]
    elif param_mode == 1:
        return param


def thruster_signal(programme, phase_settings):
    last_output = 0
    for phase_setting in phase_settings:
        last_output = run(programme.copy(), [phase_setting, last_output])[0]
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

    # code_line = '3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0'
    # code_line = '3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0'
    programme = parse(code_line)

    # print(thruster_signal(programme, [4,3,2,1,0]))
    # print(thruster_signal(programme, [0,1,2,3,4]))

    highest_signal = 0
    best_phase_sequence = []
    for phase_sequence in permutations([0,1,2,3,4]):
        signal = thruster_signal(programme, phase_sequence)
        if signal > highest_signal:
            best_phase_sequence = phase_sequence
            highest_signal = signal

    print(highest_signal, "from", best_phase_sequence)


if __name__ == "__main__":
    main()
