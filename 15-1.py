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


class Ship:
    NORTH: int = 1
    SOUTH: int = 2
    WEST: int = 3
    EAST: int = 4

    def __init__(self):
        self._tiles: dict = {XY(0, 0): 'D'}
        self._min_x = 0
        self._max_x = 0
        self._min_y = 0
        self._max_y = 0
        self.oxygen = None
        self.droid_loc = XY(0, 0)

    def get(self, coord: XY):
        if coord not in self._tiles.keys():
            return 0
        return self._tiles[coord]

    def set(self, x, y, value):
        coord = XY(x, y)
        self._tiles[coord] = value
        self._min_x = min(coord.x, self._min_x)
        self._max_x = max(coord.x, self._max_x)
        self._min_y = min(coord.y, self._min_y)
        self._max_y = max(coord.y, self._max_y)

    def draw(self):
        for y in range(self._max_y, self._min_y - 1, -1):
            for x in range(self._min_x, self._max_x + 1):
                coord = XY(x, y)
                if coord in self._tiles.keys():
                    if self.oxygen is not None and coord == self.oxygen:
                        print(Back.GREEN + 'o', end='')
                    elif coord == self.droid_loc:
                        print(Fore.GREEN + 'D', end='')
                    elif coord == XY(0, 0):
                        print(Back.RED + 'x', end='')
                    else:
                        if self.get(coord) == '.':
                            print(' ', end='')
                        else:
                            print('#', end='')
                else:
                    print(Fore.LIGHTBLACK_EX + '?', end='')
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


class Droid:
    def __init__(self, programme, ship: Ship):
        self._computer = Computer(programme, [], debug=False)
        self.ship = ship
        self.pos: XY = XY(0, 0)
        self.prev_pos: XY = XY(0, 0)
        self.visited = set()
        self.oxygen = None
        self.oil_drops = []
        self.backtracking = False

    def relative_loaction(self, direction: int):
        offset = {
            Ship.NORTH: XY(0, 1),
            Ship.SOUTH: XY(0, -1),
            Ship.WEST: XY(-1, 0),
            Ship.EAST: XY(1, 0)
        }[direction]
        return XY(self.pos.x + offset.x, self.pos.y + offset.y)

    def update(self, direction: int, status_code: int):
        old_loc = self.pos
        new_loc = self.relative_loaction(direction)

        if status_code == 0:
            self.ship.set(new_loc.x, new_loc.y, '#')
        elif status_code == 1:
            self.ship.droid_loc = new_loc
            # self.ship.set(new_loc.x, new_loc.y, 'D')
            self.ship.set(old_loc.x, old_loc.y, '.')
            self.pos = new_loc
        elif status_code == 2:
            self.ship.oxygen = new_loc
            self.ship.set(new_loc.x, new_loc.y, 'o')
            self.ship.set(old_loc.x, old_loc.y, '.')
            self.pos = new_loc

    def search(self):
        # compass_keys = {
        #     '8': Ship.NORTH,
        #     '5': Ship.SOUTH,
        #     '2': Ship.SOUTH,
        #     '4': Ship.WEST,
        #     '6': Ship.EAST
        # }

        iteration = 0
        while self._computer.state() != 'halt':
            self._computer.run()
            self.venture()
            if iteration % 100 == 0:
                self.ship.draw()
            iteration += 1

            # if self._computer.state() == 'wait':
            #     key = str(msvcrt.getch(), encoding='utf-8')
            #
            #     if key == 'q':
            #         exit()
            #     if key not in compass_keys.keys():
            #         key = '4'
            #     direction = compass_keys[key]
            # #     self._computer.input(direction)
            # #     # time.sleep(0.025)
            # # self._computer.run()
            # # status_code = self._computer.read()
            # # self.update(direction, status_code)
            # self.prev_pos = self.pos
            # self.visited.add(self.pos)
            # self.update(direction, self.try_move(direction))
            # print('\n\n')
            # # self.ship.draw()
            # # print(self.ship)

    def try_move(self, direction):
        self._computer.input(direction)
        self._computer.run()
        return self._computer.read()
    
    def venture(self):
        self.map_vicinity()

        north_pos = self.relative_loaction(Ship.NORTH)
        north_val = self.ship.get(north_pos)
        south_pos = self.relative_loaction(Ship.SOUTH)
        south_val = self.ship.get(south_pos)
        west_pos = self.relative_loaction(Ship.WEST)
        west_val = self.ship.get(west_pos)
        east_pos = self.relative_loaction(Ship.EAST)
        east_val = self.ship.get(east_pos)
        
        moves = list(filter(lambda move: move['val'] == '.', [
            {'pos': north_pos, 'val': north_val, 'direction': Ship.NORTH},
            {'pos': south_pos, 'val': south_val, 'direction': Ship.SOUTH},
            {'pos': west_pos, 'val': west_val, 'direction': Ship.WEST},
            {'pos': east_pos, 'val': east_val, 'direction': Ship.EAST}
        ]))
        visited = list(filter(lambda move: move['pos'] in self.visited, moves))
        unvisited = list(filter(lambda move: move['pos'] not in self.visited, moves))

        if len(unvisited) >= 1:
            direction = unvisited[0]['direction']
            self.backtracking = False
            self.oil_drops.append(self.pos)
            self.prev_pos = self.pos
            self.update(direction, self.try_move(direction))
            self.visited.add(self.pos)
            self._computer.run()
        else:
            backtrack = list(filter(lambda move: move['pos'] == self.oil_drops[-1],
                                    visited))[0]
            direction = backtrack['direction']
            self.backtracking = True
            self.oil_drops.pop()
            self.prev_pos = self.pos
            self.update(direction, self.try_move(direction))
            self._computer.run()

    def map_vicinity(self):
        north_code = self.try_move(Ship.NORTH)
        self._computer.run()
        self.update(Ship.NORTH, north_code)
        if north_code in [1, 2]:
            self.update(Ship.SOUTH, self.try_move(Ship.SOUTH))
            self._computer.run()

        south_code = self.try_move(Ship.SOUTH)
        self._computer.run()
        self.update(Ship.SOUTH, south_code)
        if south_code in [1, 2]:
            self.update(Ship.NORTH, self.try_move(Ship.NORTH))
            self._computer.run()

        west_code = self.try_move(Ship.WEST)
        self._computer.run()
        self.update(Ship.WEST, west_code)
        if west_code in [1, 2]:
            self.update(Ship.EAST, self.try_move(Ship.EAST))
            self._computer.run()

        east_code = self.try_move(Ship.EAST)
        self._computer.run()
        self.update(Ship.EAST, east_code)
        if east_code in [1, 2]:
            self.update(Ship.WEST, self.try_move(Ship.WEST))
            self._computer.run()


def main():
    colorama.init()

    inputFile = basename(__file__)[:2] + '-input.txt'
    lines = []
    with open(inputFile,  'r') as infile:
        for line in infile:
            lines.append(line.strip())

    programme = parse(lines[0])
    ship = Ship()
    droid = Droid(programme, ship)
    droid.search()


if __name__ == "__main__":
    main()
