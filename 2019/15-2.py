import time

import colorama
from colorama import Fore, Back


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

    def north(self):
        return self.relative_location(1)

    def south(self):
        return self.relative_location(2)

    def west(self):
        return self.relative_location(3)

    def east(self):
        return self.relative_location(4)

    def relative_location(self, direction: int):
        offset = {
            1: XY(0, 1),
            2: XY(0, -1),
            3: XY(-1, 0),
            4: XY(1, 0)
        }[direction]
        return XY(self.x + offset.x, self.y + offset.y)


class Ship:
    NORTH: int = 1
    SOUTH: int = 2
    WEST: int = 3
    EAST: int = 4

    def __init__(self):
        self._tiles: dict = {}
        self._min_x = 0
        self._max_x = 0
        self._min_y = 0
        self._max_y = 0
        self.oxygen = None

    def get(self, coord: XY):
        if coord not in self._tiles.keys():
            return 0
        return self._tiles[coord]

    def set(self, coord: XY, value):
        self._tiles[coord] = value
        self._min_x = min(coord.x, self._min_x)
        self._max_x = max(coord.x, self._max_x)
        self._min_y = min(coord.y, self._min_y)
        self._max_y = max(coord.y, self._max_y)

    def spread_oxygen(self):
        oxygens = []
        for coord, value in self._tiles.items():
            if value == 'o':
                oxygens.append(coord)

        spread_happened = False
        for coord in oxygens:
            for spread_to in [coord.north(), coord.south(), coord.west(), coord.east()]:
                if self.get(spread_to) == ' ':
                    self.set(spread_to, 'o')
                    spread_happened = True

        return spread_happened

    def tick_tock(self):
        minutes = 0
        while self.spread_oxygen():
            minutes += 1
            if minutes % 20 == 0:
                self.draw()
                time.sleep(0.2)
        self.draw()
        print(minutes, 'minutes before spreading stopped')

    def draw(self):
        for y in range(self._max_y, self._min_y - 1, -1):
            for x in range(self._min_x, self._max_x + 1):
                coord = XY(x, y)
                value = self.get(coord)
                if value == 'o':
                    print(Fore.LIGHTBLUE_EX, end='')
                print(value, end='')
                print(Fore.RESET + Back.RESET, end='')
            print('')
        print('\n\n')

    def __str__(self):
        image = ''
        for y in range(self._max_y, self._min_y - 1, -1):
            for x in range(self._min_x, self._max_x + 1):
                coord = XY(x, y)
                if coord in self._tiles.keys():
                    value = self._tiles[coord]
                    image += str(value)

            image += '\n'
        return image

    def __repr__(self):
        return self.__str__()


def main():
    colorama.init()

    inputFile = '15-2-ship.txt'
    lines = []
    with open(inputFile,  'r') as infile:
        for line in infile:
            lines.append(line.strip())

    ship = Ship()

    height = len(lines)
    width = len(lines[0])
    for i in range(0, height):
        for x in range(0, width):
            y = height - i
            ship.set(XY(x, y), lines[i][x])

    ship.tick_tock()


if __name__ == "__main__":
    main()
