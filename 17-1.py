from os.path import basename

import colorama
from colorama import Fore, Back

from computer import Computer


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


def main():
    colorama.init()

    inputFile = basename(__file__)[:2] + '-input.txt'
    lines = []
    with open(inputFile,  'r') as infile:
        for line in infile:
            lines.append(line.strip())

    programme = parse(lines[0])

    computer = Computer(programme, [], debug=False)
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


if __name__ == "__main__":
    main()
