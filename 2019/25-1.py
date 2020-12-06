from os.path import basename
from itertools import combinations

import colorama
import re

from computer import Computer


def parse(code_line):
    programme = []
    for code in code_line.split(","):
        programme.append(int(code))
    return programme


class Droid:
    def __init__(self, programme):
        self.comp = Computer(programme, [])
        self.rooms = {
            'kitchen': ['e'],
            'arcade': ['e', 'e'],
            'navigation': ['e', 'e', 'n'],
            'storage': ['e', 'e', 'n', 'w'],
            'hot chocolate factory': ['e', 'e', 'n', 'w', 'w'],
            'gift wrapping': ['n'],
            'corridor': ['n', 'e'],
            'holodeck': ['n', 'e', 'n'],
            'observatory': ['n', 'n'],
            'passages': ['n', 'n', 'n'],
            'engineering': ['w'],
            'crew quarters': ['w', 's'],
            'hallway': ['w', 'w'],
            'sick bay': ['w', 'w', 's'],
            'warp drive maintenance': ['w', 'w', 's', 'e'],
            'stables': ['w', 'w', 's', 'e', 'n'],
            'science lab': ['w', 'w', 'n'],
            'security check': ['w', 'w', 'n', 'e'],
            'psf': ['w', 'w', 'n', 'e', 'e'],
        }
        self.items = {
            'sand': 'hallway',
            'ornament': 'arcade',
            'semiconductor': 'kitchen',
            'photons': 'navigation',
            'infinite loop': 'storage',
            'giant electromagnet': 'hot chocolate factory',
            'escape pod': 'corridor',
            'loom': 'holodeck',
            'mutex': 'passages',
            'dark matter': 'science lab',
            'molten lava': 'sick bay',
            'asterisk': 'warp drive maintenance',
            'wreath': 'stables'
        }

    def north(self):
        self.command('north')

    def south(self):
        self.command('south')

    def east(self):
        self.command('east')

    def west(self):
        self.command('west')

    def drop(self, item):
        self.command('drop ' + item)

    def take(self, item):
        self.command('take ' + item)

    def inv(self):
        self.command('inv')

    def start(self):
        self.comp.run()

    def move(self, directions):
        full = {'n': 'north', 's': 'south', 'e': 'east', 'w': 'west'}
        for direction in directions:
            self.command(full[direction])

    def undo(self, directions):
        oppos = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}
        for direction in reversed(directions):
            self.move(oppos[direction])

    def move_to(self, room):
        self.move(self.rooms[room])

    def move_from(self, room):
        self.undo(self.rooms[room])

    def fetch(self, item):
        for item, room in filter(lambda i: i[0] == item, self.items.items()):
            self.move(self.rooms[room])
            self.take(item)
            self.undo(self.rooms[room])

    def ditch(self, item, room):
        self.move(self.rooms[room])
        self.drop(item)
        self.items[item] = room
        self.undo(self.rooms[room])

    def command(self, command):
        for char in command:
            self.comp.input(ord(char))
        self.comp.input(10)
        self.comp.run()

    def describe(self) -> str:
        description = ''
        while self.comp.has_output():
            description += chr(self.comp.read())
        return description

    def print(self):
        print(self.describe(), end='')


def main():
    colorama.init()

    inputFile = basename(__file__)[:2] + '-input.txt'
    lines = []
    with open(inputFile,  'r') as infile:
        for line in infile:
            lines.append(line.strip())

    programme = parse(lines[0])

    # options = ['sand', 'semiconductor', 'mutex', 'dark matter', 'wreath', 'asterisk']
    # combos = list(combinations(options, 2))
    # combos = list(combinations(options, 3))
    # for items in combos:
    #     print('combo: ', ['loom'] + list(items), end='')
    #     droid = Droid(programme.copy())
    #     droid.start()
    #
    #     droid.fetch('loom')
    #     for item in items:
    #         droid.fetch(item)
    #     droid.move_to('psf')
    #     droid.inv()
    #     match = re.search(r'(lighter|heavier)', droid.describe())
    #     print('->', 'Droids are ' + match.group(0))

    droid = Droid(programme.copy())
    droid.start()
    droid.fetch('sand')
    droid.fetch('loom')
    droid.fetch('mutex')
    droid.fetch('wreath')
    droid.move_to('psf')
    droid.inv()
    droid.print()


if __name__ == "__main__":
    main()
