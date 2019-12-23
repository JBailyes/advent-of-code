from os.path import basename
from typing import Dict

import colorama
import re

from netcomp import NetworkedComputer


def parse(code_line):
    programme = []
    for code in code_line.split(","):
        programme.append(int(code))
    return programme


def main():
    colorama.init()

    inputFile = basename(__file__)[:2] + '-input.txt'
    lines = []
    with open(inputFile,  'r') as infile:
        for line in infile:
            lines.append(line.strip())

    programme = parse(lines[0])

    computers: Dict[int, NetworkedComputer] = {}
    for addr in range(0, 50):
        print('Making ', addr)
        computers[addr] = NetworkedComputer(programme, [addr])

    done = False
    while not done:
        for addr, computer in computers.items():
            if len(computer.outputs()) >= 3:
                dest = computer.read()
                x_val = computer.read()
                y_val = computer.read()
                print('dest={0} x={1} y={2}'.format(dest, x_val, y_val))
                if dest == 255:
                    done = True
                else:
                    computers[dest].input(x_val)
                    computers[dest].input(y_val)
            computer.tick()


if __name__ == "__main__":
    main()
