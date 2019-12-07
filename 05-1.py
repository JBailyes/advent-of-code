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


POSITIONAL = 0
IMMEDIATE = 1
output_codes = []

def run(programme, input_value):
    instruction_pointer = 0
    while instruction_pointer < len(programme):
        instruction = '{0:05}'.format(programme[instruction_pointer])
        opcode = int(instruction[-2:])
        param_1_mode = int(instruction[2])
        param_2_mode = int(instruction[1])
        param_3_mode = int(instruction[0])
        print('{0}: op {1} p1m {2} p2m {3} p3m {4}'.format(
            instruction, opcode, param_1_mode, param_2_mode, param_3_mode))
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
            store_address = programme[instruction_pointer + 1]
            print('  Store {0} at {1}'.format(input_value, store_address))
            programme[store_address] = input_value
            instruction_pointer += 2
        elif opcode == 4:
            # output
            param_1 = programme[instruction_pointer + 1]
            value_1 = get_value(programme, param_1, param_1_mode)
            print('  Output: read {0} from {1}'.format(value_1, param_1))
            output_codes.append(value_1)
            instruction_pointer += 2
        elif opcode == 99:
            # instruction_pointer += 1
            return


def get_value(programme, param, param_mode):
    if param_mode == POSITIONAL:
        return programme[param]
    elif param_mode == IMMEDIATE:
        return param


def main():
    colorama.init()

    inputFile = basename(__file__)[:2] + '-input.txt'
    lines = []
    with open(inputFile, 'r') as infile:
        for line in infile:
            lines.append(line.strip())

    # lines = ["1101, 100, -1, 4, 0"]
    # lines = ["1002,4,3,4,33"]
    # lines = ["3,0,4,0,99"]

    programme = []
    for code in lines[0].split(","):
        programme.append(int(code))

    run(programme, 1)
    for output_code in output_codes:
        print('output:', output_code)


if __name__ == "__main__":
    main()
