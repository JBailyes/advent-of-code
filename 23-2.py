from os.path import basename
from typing import Dict

import colorama

from netcomp import NetworkedComputer


def parse(code_line):
    programme = []
    for code in code_line.split(","):
        programme.append(int(code))
    return programme


class NAT:
    def __init__(self):
        self.x = None
        self.y = None
        self.sent_y = []

    def send(self):
        if len(self.sent_y) > 1:
            if self.y == self.sent_y[-1]:
                print(self.y, 'delivered twice')
                exit(0)
        self.sent_y.append(self.y)


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

    nat = NAT()
    done = False
    inactivity_count = 0
    while not done:
        any_active = False
        for addr, computer in computers.items():
            any_active |= computer.has_output() | computer.has_inputs()
            if len(computer.outputs()) >= 3:
                dest = computer.read()
                x_val = computer.read()
                y_val = computer.read()
                print('dest={0} x={1} y={2}'.format(dest, x_val, y_val))
                if dest == 255:
                    nat.x = x_val
                    nat.y = y_val
                else:
                    computers[dest].input(x_val)
                    computers[dest].input(y_val)
            computer.tick()
        if not any_active:
            inactivity_count += 1
            if inactivity_count > 999:
                computers[0].input(nat.x)
                computers[0].input(nat.y)
                nat.send()
        else:
            inactivity_count = 0


if __name__ == "__main__":
    main()
