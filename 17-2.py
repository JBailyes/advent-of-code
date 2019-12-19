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

    def add(self, coord: XY, move: str):
        self.moves.append(move)
        self.visited[coord]


class Move:
    def __init__(self, direction: str, distance: int):
        self.direction = direction
        self.distance = distance

    def __str__(self):
        return self.direction + ',' + str(self.distance)

    def __eq__(self, other):
        return self.direction == other.direction and self.distance == other.distance


class Function:
    def __init__(self, moves: List[Move]):
        self.moves = moves
        self.matches: List[int] = []  # Start positions where function matches some moves
        self._coverage = set()

    def ascii_len(self):
        return len(self.__str__())

    def moves_len(self):
        return len(self.moves)

    def applies_to(self, moves: List[Move]) -> bool:
        return self.moves == moves

    def add_match(self, position):
        self.matches.append(position)

    def add_coverage(self, positions: List[int]):
        for position in positions:
            self._coverage.add(position)

    def coverage(self) -> Set[int]:
        return self._coverage

    def __str__(self):
        return ','.join([str(move) for move in self.moves])

    def __repr__(self):
        return self.__str__()


def calculate_functions(moves: List[Move]):
    functions: Dict[str, Function] = {}
    for sequence_len in range(1, 8):  # Any longer than 5 are guaranteed to be > 20 chars
        for i in range(0, len(moves) - sequence_len):
            function = Function(moves[i:i + sequence_len])
            # if function.len() > 20:
            #     continue
            if function not in functions.keys():
                functions[str(function)] = function
            functions[str(function)].matches.append(i)

    best_combo = []
    best_combo_coverage = 0
    for a, b, c in combinations(functions.values(), 3):
        possibilities = apply_functions(moves, a, b, c)
        if len(possibilities) > 0:
            print('got options:')
            for sequence in possibilities:
                print(sequence)


        # Rule-out functions that overlap
        # if a.coverage().intersection(b.coverage()):
        #     continue
        # if a.coverage().intersection(c.coverage()):
        #     continue
        # if b.coverage().intersection(c.coverage()):
        #     continue
        #
        # # Calculate how many of the moves are covered by this combo of functions
        # moves_covered = len(a.coverage() | b.coverage() | c.coverage())
        # if moves_covered > best_combo_coverage:
        #     best_combo = [a, b, c]
        #     best_combo_coverage = moves_covered

    return best_combo


def apply_functions(moves: List[Move], a: Function, b: Function, c: Function) -> List[List[Function]]:
    options = []
    for func in [a, b, c]:
        if len(moves) >= func.moves_len() and func.applies_to(moves[:func.moves_len()]):
            for sequence in apply_functions(moves[func.moves_len():], a, b, c):
                options.append([func] + sequence)
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

    # match_positions = []
    # for pattern_len in range(1, 8):
    #     found = set()
    #     for i in range(0, len(moves) - pattern_len):
    #         pattern = moves[i:i + pattern_len]
    #         pattern_str = ' '.join(pattern)
    #         if len(pattern_str.replace('  ', ' ').replace(' ', ',')
    #                        .rstrip(',').replace('L', 'L,').replace('R', 'R,')) > 20:
    #             continue
    #         if pattern_str not in found:
    #             found.add(pattern_str)
    #             matches_str = ''
    #             matches = 0
    #             moves_matched = set()
    #             j = 0
    #             while j <= len(moves) - pattern_len:
    #                 if moves[j:j + pattern_len] == pattern:
    #                     matches_str += ' '.join(pattern) + '|'
    #                     matches += 1
    #
    #                     for pos_matched in range(j, j + pattern_len):
    #                         moves_matched.add(pos_matched)
    #                     j += pattern_len
    #                 else:
    #                     matches_str += '    '
    #                     j += 1
    #                     # print(blanks, end='')
    #             if matches > 0:
    #                 print(matches_str, end=' poses:')
    #                 print(moves_matched)
    #                 match_positions.append({'positions': moves_matched, 'string': matches_str})
    #
    # best_combo_patterns = []
    # best_combo = set()
    # for patterns in combinations(match_positions, 3):
    #     if patterns[0]['positions'] & patterns[1]['positions'] or \
    #         patterns[0]['positions'] & patterns[2]['positions'] or \
    #             patterns[1]['positions'] & patterns[2]['positions']:
    #         continue
    #     combo = patterns[0]['positions'] | patterns[1]['positions'] | patterns[2]['positions']
    #     coverage = len(combo)
    #     if coverage > len(best_combo):
    #         best_combo = combo
    #         best_combo_patterns = [patterns[0], patterns[1], patterns[2]]
    # print('')
    # print('Best patterns:')
    # print(best_combo_patterns[0]['string'], best_combo_patterns[0]['positions'])
    # print(best_combo_patterns[1]['string'], best_combo_patterns[1]['positions'])
    # print(best_combo_patterns[2]['string'], best_combo_patterns[2]['positions'])


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
