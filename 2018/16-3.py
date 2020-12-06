import argparse
import re
import string
from datetime import datetime
import operator
import sys
import colorama
from colorama import Fore, Back, Style
from copy import copy


class Opcodes:
    def execute(self, reg, values):
        pass

    def addr(self, registers, a, b, c):
        out = copy(registers)
        out[c] = out[a] + out[b]
        return out

    def addi(self, registers, a, b, c):
        out = copy(registers)
        out[c] = out[a] + b
        return out

    def mulr(self, registers, a, b, c):
        out = copy(registers)
        out[c] = out[a] * out[b]
        return out

    def muli(self, registers, a, b, c):
        out = copy(registers)
        out[c] = out[a] * b
        return out

    def banr(self, registers, a, b, c):
        out = copy(registers)
        out[c] = out[a] & out[b]
        return out

    def bani(self, registers, a, b, c):
        out = copy(registers)
        out[c] = out[a] & b
        return out

    def borr(self, registers, a, b, c):
        out = copy(registers)
        out[c] = out[a] | out[b]
        return out

    def bori(self, registers, a, b, c):
        out = copy(registers)
        out[c] = out[a] | b
        return out

    def setr(self, registers, a, b, c):
        out = copy(registers)
        out[c] = out[a]
        return out

    def seti(self, registers, a, b, c):
        out = copy(registers)
        out[c] = a
        return out

    def gtir(self, registers, a, b, c):
        out = copy(registers)
        out[c] = 1 if a > out[b] else 0
        return out

    def gtri(self, registers, a, b, c):
        out = copy(registers)
        out[c] = 1 if out[a] > b else 0
        return out

    def gtrr(self, registers, a, b, c):
        out = copy(registers)
        out[c] = 1 if out[a] > out[b] else 0
        return out

    def eqir(self, registers, a, b, c):
        out = copy(registers)
        out[c] = 1 if a == out[b] else 0
        return out

    def eqri(self, registers, a, b, c):
        out = copy(registers)
        out[c] = 1 if out[a] == b else 0
        return out

    def eqrr(self, registers, a, b, c):
        out = copy(registers)
        out[c] = 1 if out[a] == out[b] else 0
        return out


class Instruction:
    def __init__(self, numbers):
        self.opcode = int(numbers[0])
        self.a = int(numbers[1])
        self.b = int(numbers[2])
        self.c = int(numbers[3])

    def __repr__(self):
        return '{0} {1} {2} {3}'.format(self.opcode, self.a, self.b, self.c)


def main():
    colorama.init()

    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()

    prog = []
    with open(args.input, 'r') as infile:
        for line in infile:
            prog.append(Instruction(line.strip().split(' ')))

    opcodes = Opcodes()

    def execute(registers, instruction):
        opcode = instruction.opcode
        a = instruction.a
        b = instruction.b
        c = instruction.c

        if opcode == 0:
            return opcodes.banr(registers, a, b, c)
        elif opcode == 1:
            return opcodes.muli(registers, a, b, c)
        elif opcode == 2:
            return opcodes.bori(registers, a, b, c)
        elif opcode == 3:
            return opcodes.setr(registers, a, b, c)
        elif opcode == 4:
            return opcodes.addi(registers, a, b, c)
        elif opcode == 5:
            return opcodes.eqrr(registers, a, b, c)
        elif opcode == 6:
            return opcodes.gtri(registers, a, b, c)
        elif opcode == 7:
            return opcodes.gtir(registers, a, b, c)
        elif opcode == 8:
            return opcodes.borr(registers, a, b, c)
        elif opcode == 9:
            return opcodes.eqri(registers, a, b, c)
        elif opcode == 10:
            return opcodes.bani(registers, a, b, c)
        elif opcode == 11:
            return opcodes.addr(registers, a, b, c)
        elif opcode == 12:
            return opcodes.eqir(registers, a, b, c)
        elif opcode == 13:
            return opcodes.mulr(registers, a, b, c)
        elif opcode == 14:
            return opcodes.seti(registers, a, b, c)
        elif opcode == 15:
            return opcodes.gtrr(registers, a, b, c)

    registers = [0, 0, 0, 0]
    for instruction in prog:
        registers = execute(registers, instruction)

    print(registers)
    print('Finish')


if __name__ == "__main__":
    main()
