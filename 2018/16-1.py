import argparse
import re
import string
from datetime import datetime
import operator
import sys
import colorama
from colorama import Fore, Back, Style
from copy import copy


class Sample:
    def __init__(self, before, instruction, after):
        self.before = before
        self.instruction = instruction
        self.after = after

    def __repr__(self):
        return 'Before: {0}, {1}, After: {2}'.format(
            self.before, self.instruction, self.after)


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


class Simulate:
    def __init__(self, before):
        self.registers = copy(before)

    def execute(self, opcode):
        pass


def main():
    colorama.init()

    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()

    lines = ''
    with open(args.input, 'r') as infile:
        for line in infile:
            lines += line.strip()

    samples = []

    sampleRegex = r'Before: \[(\d+), (\d+), (\d+), (\d+)\](\d+) (\d+) (\d+) (\d+)After:  \[(\d+), (\d+), (\d+), (\d+)\]'
    matches = re.finditer(sampleRegex, lines)
    for match in matches:
        sample = Sample(
            [int(match.group(1)), int(match.group(2)), int(match.group(3)), int(match.group(4))],
            [int(match.group(5)), int(match.group(6)), int(match.group(7)), int(match.group(8))],
            [int(match.group(9)), int(match.group(10)), int(match.group(11)), int(match.group(12))])
        samples.append(sample)

    opcodes = Opcodes()

    def findMatches(sample):
        matches = []
        before = sample.before
        after = sample.after
        a = sample.instruction[1]
        b = sample.instruction[2]
        c = sample.instruction[3]

        if after == opcodes.addr(before, a, b, c):
            matches.append('addr')

        if after == opcodes.addi(before, a, b, c):
            matches.append('addi')

        if after == opcodes.mulr(before, a, b, c):
            matches.append('mulr')

        if after == opcodes.muli(before, a, b, c):
            matches.append('muli')

        if after == opcodes.banr(before, a, b, c):
            matches.append('banr')

        if after == opcodes.bani(before, a, b, c):
            matches.append('bani')

        if after == opcodes.borr(before, a, b, c):
            matches.append('borr')

        if after == opcodes.bori(before, a, b, c):
            matches.append('bori')

        if after == opcodes.setr(before, a, b, c):
            matches.append('setr')

        if after == opcodes.seti(before, a, b, c):
            matches.append('seti')

        if after == opcodes.gtir(before, a, b, c):
            matches.append('gtir')

        if after == opcodes.gtri(before, a, b, c):
            matches.append('gtri')

        if after == opcodes.gtrr(before, a, b, c):
            matches.append('gtrr')

        if after == opcodes.eqir(before, a, b, c):
            matches.append('eqir')

        if after == opcodes.eqri(before, a, b, c):
            matches.append('eqri')

        if after == opcodes.eqrr(before, a, b, c):
            matches.append('eqrr')

        return matches


    matchesOver3 = 0
    for sample in samples:
        matches = findMatches(sample)
        if len(matches) > 2:
            matchesOver3 += 1
            print(sample)
            print('   matches {0}'.format(matches))
    print('{0} samples'.format(matchesOver3))

    print()
    print('Finish')


if __name__ == "__main__":
    main()
