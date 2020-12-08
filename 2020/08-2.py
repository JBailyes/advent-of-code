import argparse
import re
from copy import copy


class Instruction:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return '{}: {}'.format(self.name, self.value)


class Run:
    def __init__(self, programme):
        self.programme = programme
        self.accumulator = 0
        self.executed = []

    def execute(self):
        line = 0
        while True:
            if line in self.executed:
                print('line', line)
                print('previous line:', self.executed[-1])
                print('Loop. Acc:', self.accumulator)
                return None
            if line == len(self.programme):
                print('Got to the end. Acc:', self.accumulator)
                return self.accumulator
            self.executed.append(line)

            instruction = self.programme[line]
            if instruction.name == 'acc':
                self.accumulator += instruction.value
            elif instruction.name == 'jmp':
                line = line + instruction.value
                continue
            elif instruction.name == 'nop':
                pass
            line += 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()

    lines = []
    with open(args.input, 'r') as infile:
        for line in infile:
            lines.append(line.strip())

    programme = []
    for line in lines:
        (op, val) = line.split(' ', maxsplit=1)
        programme.append(Instruction(op, int(val)))

    def swap_instruction(instruction):
        op_swap = {
            'acc': 'acc',
            'jmp': 'nop',
            'nop': 'jmp'
        }
        return Instruction(op_swap[instruction.name], instruction.value)

    for replacement_line in range(len(programme)):
        print('Replacing line', replacement_line)
        programme_copy = copy(programme)
        programme_copy[replacement_line] = swap_instruction(programme[replacement_line])
        output = Run(programme_copy).execute()  # 1125
        if output is not None:
            exit()
        print()


if __name__ == "__main__":
    main()
