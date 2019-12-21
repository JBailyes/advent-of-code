from os.path import basename

import colorama
import re

from computer import Computer


def parse(code_line):
    programme = []
    for code in code_line.split(","):
        programme.append(int(code))
    return programme


class Springdroid:
    def __init__(self, intcode_prog):
        self.comp = Computer(intcode_prog, [])
        self.comp.run()  # Gets it to the initial state where it asks for input

    def load(self, springscript: str):
        for full_line in springscript.splitlines(keepends=True):
            line = full_line.strip()
            if re.search(r'^#', line):  # Comment line
                continue
            code = line.split('#')[0].strip()  # Chop off end-of-line comments
            if code != '':
                self.ss_line(code)

    def ss_line(self, instruction: str):
        for char in instruction.upper():
            self.comp.input(ord(char))
        if not instruction.endswith('\n'):
            self.comp.input(ord('\n'))

    def read_ascii(self):
        output = ''
        while self.comp.has_output():
            if self.comp.outputs()[0] < 255:
                output += str(chr(self.comp.read()))
            else:
                return output
        return output

    def print_out(self):
        print(self.read_ascii())
        if self.comp.has_output():
            print(self.comp.read())

    def run(self):
        self.comp.run()


def main():
    colorama.init()

    inputFile = basename(__file__)[:2] + '-input.txt'
    lines = []
    with open(inputFile,  'r') as infile:
        for line in infile:
            lines.append(line.strip())

    springscript = """
        not c j
        and d j
        not a t
        or t j
        walk
    """

    programme = parse(lines[0])
    droid = Springdroid(programme)
    droid.print_out()
    droid.load(springscript)
    droid.run()
    droid.print_out()


if __name__ == "__main__":
    main()
