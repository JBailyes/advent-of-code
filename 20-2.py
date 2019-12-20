import string
from os.path import basename
from typing import Dict, List, Set

import colorama
from colorama import Fore, Back


class XY:
    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return str(self.x) + ',' + str(self.y) + ',' + str(self.z)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __hash__(self):
        return hash(str(self.x) + ',' + str(self.y) + ',' + str(self.z))

    def up(self):
        return self.relative_location(1)

    def down(self):
        return self.relative_location(2)

    def left(self):
        return self.relative_location(3)

    def right(self):
        return self.relative_location(4)

    def descend(self):
        return XY(self.x, self.y, self.z + 1)

    def ascend(self):
        return XY(self.x, self.y, self.z - 1)

    def to_level(self, level):
        return XY(self.x, self.y, level)

    def relative_location(self, direction: int):
        offset = {
            1: XY(0, -1),
            2: XY(0, 1),
            3: XY(-1, 0),
            4: XY(1, 0)
        }[direction]
        return XY(self.x + offset.x, self.y + offset.y, self.z)


class Path:
    def __init__(self, coords: List[XY]):
        self.steps: List[XY] = coords
        self.end = self.steps[-1]

    def includes(self, pos) -> bool:
        return pos in self.steps

    def len(self):
        return len(self.steps)

    def extend(self, pos):
        return Path(self.steps + [pos])

    def __repr__(self):
        return '[{0}]'.format('|'.join([str(pos) for pos in self.steps]))


class Tile:
    def __init__(self, pos: XY, level: int, value: str):
        self.pos = pos
        self.links: List[Tile] = []
        self.val = value
        self.level = level
        self.portal: Portal = None
    
    def link(self, other):
        if other not in self.links:
            self.links.append(other)
        if self not in other.links:
            other.links.append(self)

    def is_portal(self):
        return self.portal is not None

    def __eq__(self, other):
        return self.pos == other.pos

    def __str__(self):
        return '[{0}({1}) -> ({2})]'.format(self.pos, self.val, '),('.join(
            [str(link.pos) for link in self.links]))


class Portal:
    def __init__(self, name):
        self.name: str = name
        self.inner: XY = None
        self.outer: XY = None

    def other_end(self, from_pos: XY):
        if self.inner == from_pos.to_level(0):
            return self.outer
        return self.inner

    def is_outer(self, pos: XY):
        return self.outer == pos.to_level(0)

    def is_inner(self, pos: XY):
        return self.inner == pos.to_level(0)


class Maze:

    def __init__(self):
        self._tiles: Dict[XY, str] = {}
        self.min_x = None
        self.max_x = None
        self.min_y = None
        self.max_y = None

    def tile_locations(self):
        return self._tiles.keys()

    def get(self, coord: XY) -> str:
        if coord not in self._tiles.keys():
            return ' '
        return self._tiles[coord]

    def is_wall(self, coord: XY) -> bool:
        return self._tiles[coord] == '#'

    def set(self, pos: XY, value: str):
        self._tiles[pos] = value
        if self.min_x is None:
            self.min_x = pos.x
        else:
            self.min_x = min(pos.x, self.min_x)

        if self.max_x is None:
            self.max_x = pos.x
        else:
            self.max_x = max(pos.x, self.max_x)

        if self.min_y is None:
            self.min_y = pos.y
        else:
            self.min_y = min(pos.y, self.min_y)

        if self.max_y is None:
            self.max_y = pos.y
        else:
            self.max_y = max(pos.y, self.max_y)

    def draw(self):
        for y in range(self.min_y, self.max_y + 1):
            for x in range(self.min_x, self.max_x + 1):
                coord = XY(x, y)
                value = self.get(coord)
                print(value, end='')
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


solved_states: Dict[str, int] = {}


class Tiles:
    def __init__(self):
        self.tiles: Dict[XY, Tile] = {}

    def add(self, tile: Tile):
        self.tiles[tile.pos] = tile

    def get_all(self) -> List[Tile]:
        return list(self.tiles.values())

    def tile_at(self, pos: XY) -> Tile:
        return self.tiles[XY(pos.x, pos.y)]

    def all_positions(self) -> List[XY]:
        return list(self.tiles.keys())


def minimum_to_zz(start: XY, end: XY, tiles: Tiles) -> int:
    in_progress_paths: List[Path] = [Path([start])]
    positions_visited: Set[XY] = {start}
    while len(in_progress_paths) > 0:
        paths_to_continue: List[Path] = []
        for path in in_progress_paths:
            pos = path.end
            current_level = pos.z
            current_tile = tiles.tile_at(pos)
            linked_tile_positions: List[XY] = []
            if current_tile.is_portal():
                portal = current_tile.portal
                other_end = portal.other_end(pos)
                if portal.is_inner(pos):
                    linked_tile_positions.append(other_end.to_level(current_level + 1))
                elif current_level > 0:
                    linked_tile_positions.append(other_end.to_level(current_level - 1))
            linked_tile_positions += [link.pos.to_level(current_level) for link in tiles.tile_at(pos).links]

            for linked_tile_pos in linked_tile_positions:
                if linked_tile_pos not in positions_visited:  # If got here earlier then this path won't be shorter
                    if linked_tile_pos == end:  # Found the end portal
                        print('end path:', path)
                        return path.len()
                    else:
                        paths_to_continue.append(path.extend(linked_tile_pos))  # Keep going
                        positions_visited.add(linked_tile_pos)

        in_progress_paths = paths_to_continue
    return -1


def main():
    colorama.init()

    maze = Maze()

    inputFile = basename(__file__)[:2] + '-input.txt'
    # inputFile = basename(__file__)[:2] + '-1-example-1.txt'  # 26
    # inputFile = basename(__file__)[:2] + '-2-example-2.txt'  # 396

    y = 1
    with open(inputFile,  'r') as infile:
        for line in infile:
            for x, val in enumerate(line.rstrip()):
                pos = XY(x + 1, y)
                maze.set(pos, val)
            y += 1

    maze.draw()
    outer_x = [maze.min_x + 1, maze.max_x - 1]
    outer_y = [maze.min_y + 1, maze.max_y - 1]
    print('outer x', outer_x)
    print('outer y', outer_y)

    portals: Dict[str, Portal] = {}
    tiles: Tiles = Tiles()
    
    for pos in maze.tile_locations():
        val = maze.get(pos)
        if val in ' #':
            continue
        tile = Tile(pos, 0, val)
        val_up = maze.get(pos.up())
        val_down = maze.get(pos.down())
        val_left = maze.get(pos.left())
        val_right = maze.get(pos.right())
        if val in string.ascii_uppercase:
            if val_down == '.':
                label_for = pos.down()
                name = val_up + val
            elif val_up == '.':
                label_for = pos.up()
                name = val + val_down
            elif val_right == '.':
                label_for = pos.right()
                name = val_left + val
            elif val_left == '.':
                label_for = pos.left()
                name = val + val_right
            else:
                continue

            outer_tile = False
            if pos.y in outer_y or pos.x in outer_x:
                outer_tile = True
            if name not in portals.keys():
                portals[name] = Portal(name)
            if outer_tile:
                portals[name].outer = label_for
            else:
                portals[name].inner = label_for
            tile.val = name
        else:
            tiles.add(tile)
            for adjacent in [pos.up(), pos.down(), pos.left(), pos.right()]:
                if adjacent in tiles.all_positions():
                    tile.link(tiles.tile_at(adjacent))

    start: Tile = None
    end: Tile = None
    for name, portal in portals.items():
        print(name, 'inner', portal.inner, 'outer', portal.outer)
        if name in ['AA', 'ZZ']:
            if portal.inner:
                end1 = tiles.tile_at(portal.inner)
            else:
                end1 = tiles.tile_at(portal.outer)
            if name == 'AA':
                start = end1
            else:
                end = end1
        else:
            inner_tile = tiles.tile_at(portal.inner)
            outer_tile = tiles.tile_at(portal.outer)
            inner_tile.portal = portal
            outer_tile.portal = portal

    for tile in tiles.get_all():
        print(tile)

    print(minimum_to_zz(start.pos, end.pos, tiles))


if __name__ == "__main__":
    main()
