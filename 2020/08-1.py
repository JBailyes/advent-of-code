import argparse
import re


class Instruction:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return '{}: {}'.format(self.name, self.value)


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

    accumulator = 0
    executed = []

    running = True
    line = 0
    while running:
        if line in executed:
            print(executed[-1])
            exit
        executed.append(line)
        instruction = programme[line]
        if instruction.name == 'acc':
            accumulator += instruction.value
        elif instruction.name == 'jmp':
            line = line + instruction.value
            continue
        elif instruction.name == 'nop':
            pass
        line += 1


if __name__ == "__main__":
    main()
