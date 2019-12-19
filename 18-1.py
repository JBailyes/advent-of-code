from os.path import basename

import colorama
from colorama import Fore, Back
from copy import deepcopy
from computer import Computer
from itertools import combinations
from typing import Dict, List, Set
import string


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


class Path:
    def __init__(self, coords: List[XY], target: str):
        self.steps: List[XY] = coords
        self.end = self.steps[-1]
        self.target: str = target

    def __repr__(self):
        return '[{0}]'.format('|'.join([str(pos) for pos in self.steps]))


class Caves:

    def __init__(self):
        self._tiles: dict = {}
        self.min_x = 0
        self.max_x = 0
        self.min_y = 0
        self.max_y = 0
        self.keys: Dict[str, XY] = {}
        self.doors: Dict[str, XY] = {}
        self.entrance: XY = None
        self.me: XY = None

    def tile_locations(self):
        return self._tiles.keys()

    def get(self, coord: XY) -> str:
        if coord not in self._tiles.keys():
            return '.'
        return self._tiles[coord]

    def is_wall(self, coord: XY) -> bool:
        return self._tiles[coord] == '#'

    def set(self, pos: XY, value):
        self._tiles[pos] = value
        if value in string.ascii_lowercase:
            self.keys[value] = pos
        elif value in string.ascii_uppercase:
            self.doors[value] = pos
        elif value == '@':
            self.entrance = pos
            self.me = pos
        self.min_x = min(pos.x, self.min_x)
        self.max_x = max(pos.x, self.max_x)
        self.min_y = min(pos.y, self.min_y)
        self.max_y = max(pos.y, self.max_y)

    def draw(self):
        for y in range(self.max_y, self.min_y - 1, -1):
            for x in range(self.min_x, self.max_x + 1):
                coord = XY(x, y)
                value = self.get(coord)
                if value in string.ascii_lowercase:
                    print(Fore.GREEN, end='')
                elif value in string.ascii_uppercase:
                    print(Fore.LIGHTRED_EX, end='')
                elif value == '@':
                    print(Fore.CYAN, end='')
                elif self.get(coord) in '.#':
                    print(Fore.LIGHTBLACK_EX, end='')
                print(self.get(coord), end='')
                print(Fore.RESET + Back.RESET, end='')
            print('')
        print('\n\n')

    def __str__(self):
        image = ''
        for y in range(self.max_y, self.min_y - 1, -1):
            for x in range(self.min_x, self.max_x + 1):
                coord = XY(x, y)
                if coord in self._tiles.keys():
                    value = self._tiles[coord]
                    image += str(value)

            image += '\n'
        return image

    def __repr__(self):
        return self.__str__()


class CavesState:
    """ Hold state about the keys and doors in a cave """

    def __init__(self, caves: Caves, keys: Dict[str, XY], doors: Dict[str, XY], current_pos: XY):
        self.caves = caves
        self.doors = doors
        self.keys = keys
        self.keys_by_pos = {}
        for key, pos in keys.items():
            self.keys_by_pos[pos] = key
        self.doors_by_pos = {}
        for door, pos in doors.items():
            self.doors_by_pos[pos] = door
        self.position = current_pos

    def hash_string(self) -> str:
        return ''.join([key for key in self.keys.keys()]) + ''.join([door for door in self.doors.keys()]) + str(self.position)

    def is_key(self, pos: XY) -> bool:
        return pos in self.keys_by_pos.keys()

    def is_door(self, pos: XY) -> bool:
        return pos in self.doors_by_pos.keys()

    def get_key(self, pos: XY) -> str:
        return self.keys_by_pos[pos]

    def get_door(self, pos: XY) -> str:
        return self.doors_by_pos[pos]
    
    def collect_key(self, path: Path):
        # self.draw()
        key = self.keys_by_pos[path.end]
        door = key.upper()
        updated_keys = self.keys.copy()
        updated_doors = self.doors.copy()
        if door in updated_doors.keys():
            del updated_doors[door]
        del updated_keys[key]
        return CavesState(self.caves, updated_keys, updated_doors, path.end)

    def find_keys(self) -> List[Path]:
        paths: List[Path] = []
        in_progress_paths: List[List[XY]] = [[self.position]]
        positions_visited: Set[XY] = {self.position}
        while len(in_progress_paths) > 0:
            for path in in_progress_paths:
                pos = path[-1]
                for neighbour in [pos.up(), pos.down(), pos.left(), pos.right()]:
                    if neighbour not in positions_visited:  # Got here earlier, so this path won't be shorter
                        if self.caves.is_wall(neighbour) or self.is_door(neighbour):  # Dead end
                            continue
                        if self.is_key(neighbour):  # Found a key
                            paths.append(Path(path[1:] + [neighbour], self.get_key(neighbour)))
                        else:
                            in_progress_paths.append(path + [neighbour])  # Keep going
                        positions_visited.add(neighbour)
                in_progress_paths.remove(path)  # Either extended paths were spawned or we got a dead-end
        return paths
    
    def draw(self):
        for y in range(self.caves.min_y, self.caves.max_y + 1,):
            for x in range(self.caves.min_x, self.caves.max_x + 1):
                pos = XY(x, y)
                if self.is_key(pos):
                    print(Fore.YELLOW + self.keys_by_pos[pos], end='')
                elif self.is_door(pos):
                    print(Fore.LIGHTRED_EX + self.doors_by_pos[pos], end='')
                elif self.position == pos:
                    print(Fore.CYAN + '@', end='')
                elif self.caves.get(pos) in '.#':
                    print(Fore.LIGHTBLACK_EX + self.caves.get(pos), end='')
                print(Fore.RESET + Back.RESET, end='')
            print('')
        print('\n')


solved_states: Dict[str, int] = {}


def minimum_steps(caves_state: CavesState) -> int:
    state_hash = caves_state.hash_string()
    if state_hash in solved_states:
        return solved_states[state_hash]
    paths_to_keys = caves_state.find_keys()
    if len(paths_to_keys) == 0:  # All the keys have been collected
        return 0
    if len(paths_to_keys) == 1:
        path_to_key = paths_to_keys[0]
        steps = len(path_to_key.steps) + minimum_steps(caves_state.collect_key(path_to_key))
        solved_states[state_hash] = steps
        return steps
    smallest_steps_to_complete = None
    for path_to_key in paths_to_keys:
        steps = len(path_to_key.steps) + minimum_steps(caves_state.collect_key(path_to_key))
        if smallest_steps_to_complete is None or steps < smallest_steps_to_complete:
            smallest_steps_to_complete = steps
    solved_states[state_hash] = smallest_steps_to_complete
    return smallest_steps_to_complete


def main():
    colorama.init()

    caves = Caves()

    inputFile = basename(__file__)[:2] + '-input.txt'
    # inputFile = basename(__file__)[:2] + '-1-example-4.txt'
    keys = {}
    doors = {}
    y = 0
    with open(inputFile,  'r') as infile:
        for line in infile:
            for x, val in enumerate(line.strip()):
                pos = XY(x, y)
                if val in '#.':
                    caves.set(pos, val)
                else:
                    if val in string.ascii_lowercase:
                        keys[val] = pos
                    elif val in string.ascii_uppercase:
                        doors[val] = pos
                    elif val in '@':
                        caves.entrance = pos
                    caves.set(pos, '.')
            y += 1

    caves.draw()
    initial_state = CavesState(caves, keys.copy(), doors.copy(), caves.entrance)
    print(minimum_steps(initial_state))

    # 5210 too high


if __name__ == "__main__":
    main()
