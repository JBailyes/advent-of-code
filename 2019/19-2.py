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
        self._min_x = None
        self._max_x = None
        self._min_y = None
        self._max_y = None

    def pixels_xy(self):
        return self._pixels.keys()

    def get(self, coord: XY):
        if coord not in self._pixels.keys():
            return '.'
        return self._pixels[coord]

    def set(self, coord: XY, value):
        self._pixels[coord] = value
        if self._min_x is None:
            self._min_x = coord.x
        else:
            self._min_x = min(coord.x, self._min_x)

        if self._max_x is None:
            self._max_x = coord.x
        else:
            self._max_x = max(coord.x, self._max_x)

        if self._min_y is None:
            self._min_y = coord.y
        else:
            self._min_y = min(coord.y, self._min_y)

        if self._max_y is None:
            self._max_y = coord.y
        else:
            self._max_y = max(coord.y, self._max_y)

    def draw(self):
        for y in range(self._min_y, self._max_y + 1):
            for x in range(self._min_x, self._max_x + 1):
                coord = XY(x, y)
                value = self.get(coord)
                if value == 1:
                    print(Fore.CYAN + '1', end='')
                elif value == 0:
                    print(Fore.LIGHTBLACK_EX + '0', end='')
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


def main():
    colorama.init()

    inputFile = basename(__file__)[:2] + '-input.txt'
    lines = []
    with open(inputFile,  'r') as infile:
        for line in infile:
            lines.append(line.strip())

    programme = parse(lines[0])

    image = Image()

    m1 = 0.48
    m2 = 0.36
    y = 0
    width = 0
    while width < 300:
        x1 = y/m1
        x2 = y/m2
        width = x2 - x1
        y += 1
    print('at y={0} x1={1} x2={2} width={3}'.format(y, x1, x2, width))

    y1 = 411
    for y in [y1, y1 + 99]:
        for x in range(910, 1250):
            computer = Computer(programme.copy(), [], debug=False)
            computer.input(x)
            computer.input(y)
            computer.run()
            val = computer.read()
            image.set(XY(x, y), val)

    extents = []
    for y in [y1, y1 + 99]:
        print('y', y)
        left = None
        right = None
        for x in range(0, 1250):
            coord = XY(x, y)
            value = image.get(coord)
            if value == 1:
                print(Fore.CYAN + '1', end='')
                if left is None:
                    left = x
                right = x
            # elif value == 0:
            else:
                print(Fore.LIGHTBLACK_EX + '.', end='')
            print(Fore.RESET + Back.RESET, end='')
        extents.append((left, right))
        print('')
        print('tractor range {0} to {1}'.format(left, right))
    print('\n\n')
    y1_end = extents[0][1]
    y2_start = extents[1][0]
    print('y2 start: ', y2_start)
    print('overlap', (y1_end - y2_start) + 1)

    # 1081 * 10000 + 414 = 10810414 too high
    # print(y2_start * 10_000 + y1)  # 10790413 too high
    print(y2_start * 10_000 + y1)  # 10730411


if __name__ == "__main__":
    main()
