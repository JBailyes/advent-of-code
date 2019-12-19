from os.path import basename

import colorama
from colorama import Fore, Back

from computer import Computer
from itertools import combinations
from typing import Dict, List, Set

def parse(code_line):
    programme = []
    for code in code_line.split(","):
        programme.append(int(code))
    return programme


class XY:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return str(self.x) + ',' + str(self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(str(self.x) + ',' + str(self.y))

    def up(self):
        return self.relative_location(1)

    def down(self):
        return self.relative_location(2)

    def left(self):
        return self.relative_location(3)

    def right(self):
        return self.relative_location(4)

    def relative_location(self, direction: int):
        offset = {
            1: XY(0, -1),
            2: XY(0, 1),
            3: XY(-1, 0),
            4: XY(1, 0)
        }[direction]
        return XY(self.x + offset.x, self.y + offset.y)


class Image:

    def __init__(self):
        self._pixels: dict = {}
        self._min_x = 0
        self._max_x = 0
        self._min_y = 0
        self._max_y = 0
        self.oxygen = None
        self.droid_loc = XY(0, 0)

    def pixels_xy(self):
        return self._pixels.keys()

    def get(self, coord: XY):
        if coord not in self._pixels.keys():
            return '.'
        return self._pixels[coord]

    def set(self, coord: XY, value):
        self._pixels[coord] = value
        self._min_x = min(coord.x, self._min_x)
        self._max_x = max(coord.x, self._max_x)
        self._min_y = min(coord.y, self._min_y)
        self._max_y = max(coord.y, self._max_y)

    def draw(self):
        for y in range(self._max_y, self._min_y - 1, -1):
            for x in range(self._min_x, self._max_x + 1):
                coord = XY(x, y)
                value = self.get(coord)
                if value in '^<v>':
                    print(Fore.GREEN, end='')
                elif self.get(coord) == '.':
                    print(Fore.LIGHTBLACK_EX, end='')
                print(self.get(coord), end='')
                print(Fore.RESET + Back.RESET, end='')
            print('')
        print('\n\n')

    def __str__(self):
        image = ''
        for y in range(self._max_y, self._min_y - 1, -1):
            for x in range(self._min_x, self._max_x + 1):
                coord = XY(x, y)
                if coord in self._pixels.keys():
                    value = self._pixels[coord]
                    image += str(value)

            image += '\n'
        return image

    def __repr__(self):
        return self.__str__()


class Intersection:
    def __init__(self, pos: XY):
        self.pos = pos

    def alignment_param(self) -> int:
        return self.pos.x * self.pos.y


class Route:
    def __init__(self):
        self.moves: List[str] = []
        self.visited: Dict[XY, int] = {}


class Move:
    def __init__(self, direction: str, distance: int):
        self.direction = direction
        self.distance = distance
        self.ascii: str = self.direction + ',' + str(self.distance)
        self.str = self.direction + str(self.distance)

    def __str__(self):
        return self.str

    def __repr__(self):
        return self.str

    def __eq__(self, other):
        return self.direction == other.direction and self.distance == other.distance


class Function:
    def __init__(self, moves: List[Move]):
        self.moves = moves
        self.matches: List[int] = []  # Start positions where function matches some moves
        self._coverage = set()
        self.ascii = ','.join([move.ascii for move in self.moves])
        self.str = ' '.join([move.str for move in self.moves])

    def ascii_len(self):
        return len(self.ascii)

    def moves_len(self):
        return len(self.moves)

    def applies_to(self, moves: List[Move]) -> bool:
        if len(moves) != len(self.moves):
            return False
        for i, func_move in enumerate(self.moves):
            if func_move != moves[i]:
                return False
        return True

    def add_match(self, position):
        self.matches.append(position)

    def add_coverage(self, positions: List[int]):
        for position in positions:
            self._coverage.add(position)

    def coverage(self) -> Set[int]:
        return self._coverage

    def __str__(self):
        return self.str

    def __repr__(self):
        return self.str


def calculate_functions(moves: List[Move]):
    functions: Dict[str, Function] = {}
    for sequence_len in range(1, 9):  # Any longer than 5 are guaranteed to be > 20 chars
        for i in range(0, len(moves) - sequence_len):
            function = Function(moves[i:i + sequence_len])
            # if function.ascii_len() > 20:
            #     continue
            if function not in functions.keys():
                functions[str(function)] = function
            functions[str(function)].matches.append(i)

    viable_combo = []

    # a = Function([
    #     Move('L', 12), Move('R', 12), Move('L', 12)
    # ])
    # b = Function([
    #     Move('R', 12), Move('R', 12), Move('L', 12), Move('R', 8), Move('R', 8),
    #     Move('L', 12), Move('R', 8), Move('R', 8)
    # ])
    # c = Function([
    #     Move('R', 10), Move('L', 8), Move('L', 12)
    # ])

    for a, b, c in combinations(functions.values(), 3):
        possibilities = apply_functions(moves, a, b, c)
        if len(possibilities) > 0:
            print('got options:')
            for sequence in possibilities:
                print(sequence)
        viable_combo = possibilities[0]

    return viable_combo


def apply_functions(moves: List[Move], a: Function, b: Function, c: Function) -> List[List[Function]]:
    options = []
    for func in [a, b, c]:
        if len(moves) == func.moves_len():
            applies = func.applies_to(moves)
            if applies:
                options.append([func])
        elif len(moves) > func.moves_len():
            next_moves = moves[:func.moves_len()]
            applies = func.applies_to(next_moves)
            if applies:
                matching_sequences = apply_functions(moves[func.moves_len():], a, b, c)
                for matching_sequence in matching_sequences:
                    options.append([func] + matching_sequence)
    return options


def main():
    colorama.init()

    move_strings = [
        'L12', 'R12', 'L12', 'R12', 'R12', 'L12', 'R8 ', 'R8 ', 'L12', 'R8 ', 'R8 ', 'R10', 'L8 ', 'L12', 'R10', 'L8 ',
        'L12', 'R12', 'R12', 'L12', 'R8 ', 'R8 ', 'L12', 'R8 ', 'R8 ', 'R10', 'L8 ', 'L12', 'R12', 'R12', 'L12', 'R8 ',
        'R8 ', 'L12', 'R8 ', 'R8 '
    ]
    print(' '.join(move_strings))

    moves = []
    for move_str in move_strings:
        moves.append(Move(move_str[0], int(move_str.strip()[1:])))
    functions = calculate_functions(moves)
    for function in functions:
        print(function)

    # No viabe options - Need a new route around the scaffold
    exit()

    inputFile = basename(__file__)[:2] + '-input.txt'
    lines = []
    with open(inputFile,  'r') as infile:
        for line in infile:
            lines.append(line.strip())

    programme = parse(lines[0])
    computer = Computer(programme.copy(), [], debug=False)
    computer.run()
    image = Image()

    raw_image = ''

    y = 0
    x = 0
    while computer.has_output():
        char = str(chr(computer.read()))
        raw_image += char
        if char == '\n':
            y += 1
            x = 0
            continue
        image.set(XY(x, y), char)
        x += 1

    inters = []
    for coord in image.pixels_xy():
        if image.get(coord) in '#<>^v':
            if image.get(coord.up()) + image.get(coord.down()) + \
               image.get(coord.left()) + image.get(coord.right()) == '####':
                image.set(coord, 'O')
                inters.append(Intersection(coord))

    image.draw()

    sum = 0
    for inter in inters:
        sum += inter.alignment_param()

    print(sum)

    programme[0] = 2
    computer = Computer(programme.copy(), [], debug=False)


if __name__ == "__main__":
    main()
