from os.path import basename
from typing import Dict, List, Set

import colorama


class XY:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return str(self.x) + ',' + str(self.y)

    def __repr__(self):
        return self.__str__()

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


class Eris:

    def __init__(self):
        self.tiles: Dict[XY, int] = {}
        self.min_x = 0
        self.max_x = 4
        self.min_y = 0
        self.max_y = 4
        self.inner_eris: Eris = None
        self.outer_eris: Eris = None
        for y in range(0, 5):
            for x in range(0, 5):
                pos = XY(x, y)
                self.tiles[pos] = 0
        self.next_state: Dict[XY, int] = {}

    def bug_count(self):
        count = 0
        for tile in self.tiles.values():
            count += tile
        return count

    def get(self, pos: XY) -> int:
        return self.tiles[pos]
    
    def outer_left_bugs(self) -> int:
        bug_count = 0
        for pos in [XY(0, 0), XY(0, 1), XY(0, 2), XY(0, 3), XY(0, 4)]:
            bug_count += self.bugs(pos)
        return bug_count
    
    def inner_eris_outer_left_bugs(self) -> int:
        if self.inner_eris is None:
            return 0
        return self.inner_eris.outer_left_bugs()
    
    def outer_right_bugs(self) -> int:
        bug_count = 0
        for pos in [XY(4, 0), XY(4, 1), XY(4, 2), XY(4, 3), XY(4, 4)]:
            bug_count += self.bugs(pos)
        return bug_count
    
    def inner_eris_outer_right_bugs(self) -> int:
        if self.inner_eris is None:
            return 0
        return self.inner_eris.outer_right_bugs()
    
    def outer_top_bugs(self) -> int:
        bug_count = 0
        for pos in [XY(0, 0), XY(1, 0), XY(2, 0), XY(3, 0), XY(4, 0)]:
            bug_count += self.bugs(pos)
        return bug_count
    
    def inner_eris_outer_top_bugs(self) -> int:
        if self.inner_eris is None:
            return 0
        return self.inner_eris.outer_top_bugs()
    
    def outer_bottom_bugs(self) -> int:
        bug_count = 0
        for pos in [XY(0, 4), XY(1, 4), XY(2, 4), XY(3, 4), XY(4, 4)]:
            bug_count += self.bugs(pos)
        return bug_count
    
    def inner_eris_outer_bottom_bugs(self) -> int:
        if self.inner_eris is None:
            return 0
        return self.inner_eris.outer_bottom_bugs()

    def bugs(self, pos: XY) -> int:
        if pos not in self.tiles.keys():  # Outer Eris
            if self.outer_eris is None:
                return 0
            else:
                if pos.x == -1:
                    outer_x = 1
                elif pos.x == 5:
                    outer_x = 3
                else:
                    outer_x = 2
                if pos.y == -1:
                    outer_y = 1
                elif pos.y == 5:
                    outer_y = 3
                else:
                    outer_y = 2
                return self.outer_eris.bugs(XY(outer_x, outer_y))
        return self.tiles[pos]

    def set(self, pos: XY, bug: int):
        self.tiles[pos] = bug

    def __str__(self):
        image = ''
        display_chars = ['.', '#']
        for y in range(self.min_y, self.max_y + 1):
            for x in range(self.min_x, self.max_x + 1):
                coord = XY(x, y)
                image += display_chars[self.tiles[coord]]
            image += '\n'
        return image

    def __repr__(self):
        return self.__str__()

    def calculate_for_pos(self, pos: XY, adjacent_bugs: int):
        if self.tiles[pos] == 1 and adjacent_bugs != 1:
            self.next_state[pos] = 0
        elif self.tiles[pos] == 0 and adjacent_bugs in [1, 2]:
            self.next_state[pos] = 1
        else:
            self.next_state[pos] = self.tiles[pos]

    def calculate_inner(self):
        # inner ring positions that border inner Eris

        pos = XY(2, 1)
        adjacent_bugs = self.inner_eris_outer_top_bugs()
        for adj in [pos.up(), pos.left(), pos.right()]:
            adjacent_bugs += self.bugs(adj)
        self.calculate_for_pos(pos, adjacent_bugs)

        pos = XY(1, 2)
        adjacent_bugs = self.inner_eris_outer_left_bugs()
        for adj in [pos.up(), pos.down(), pos.left()]:
            adjacent_bugs += self.bugs(adj)
        self.calculate_for_pos(pos, adjacent_bugs)

        pos = XY(3, 2)
        adjacent_bugs = self.inner_eris_outer_right_bugs()
        for adj in [pos.up(), pos.down(), pos.right()]:
            adjacent_bugs += self.bugs(adj)
        self.calculate_for_pos(pos, adjacent_bugs)

        pos = XY(2, 3)
        adjacent_bugs = self.inner_eris_outer_bottom_bugs()
        for adj in [pos.down(), pos.left(), pos.right()]:
            adjacent_bugs += self.bugs(adj)
        self.calculate_for_pos(pos, adjacent_bugs)

        if self.inner_eris is None:
            inner_ring_bugs = 0
            for pos in [XY(2, 1), XY(1, 2), XY(3, 2), XY(2, 3)]:
                inner_ring_bugs += self.bugs(pos)
            if inner_ring_bugs > 0:  # Infestation spreads to inner Eris
                self.inner_eris = Eris()
                self.inner_eris.outer_eris = self

    def calculate_outer(self):
        outer_ring = [XY(0, 0), XY(1, 0), XY(2, 0), XY(3, 0), XY(4, 0),
                      XY(0, 1),                               XY(4, 1),
                      XY(0, 2),                               XY(4, 2),
                      XY(0, 3),                               XY(4, 3),
                      XY(0, 4), XY(1, 4), XY(2, 4), XY(3, 4), XY(4, 4)]

        for pos in outer_ring + [XY(1, 1), XY(3, 1), XY(1, 3), XY(3, 3)]:
            adjacent_bugs = 0
            for adj in [pos.up(), pos.down(), pos.left(), pos.right()]:
                adjacent_bugs += self.bugs(adj)
            self.calculate_for_pos(pos, adjacent_bugs)

        if self.outer_eris is None:
            edge_bugs = [0, 0, 0, 0]
            for pos in filter(lambda p: p.x == 0, outer_ring):
                edge_bugs[0] += self.bugs(pos)
            for pos in filter(lambda p: p.x == 4, outer_ring):
                edge_bugs[1] += self.bugs(pos)
            for pos in filter(lambda p: p.y == 0, outer_ring):
                edge_bugs[2] += self.bugs(pos)
            for pos in filter(lambda p: p.y == 4, outer_ring):
                edge_bugs[3] += self.bugs(pos)

            if 1 in edge_bugs or 2 in edge_bugs:  # Infestation spreads to outer Eris
                self.outer_eris = Eris()
                self.outer_eris.inner_eris = self

    def apply(self):
        for pos, bug in self.next_state.items():
            self.tiles[pos] = bug
        self.next_state = {}


def draw(eris):
    levels = {}

    level = 0
    levels[level] = str(eris)

    inner = eris.inner_eris
    while inner is not None:
        level += 1
        levels[level] = str(inner)
        inner = inner.inner_eris

    level = 0
    outer = eris.outer_eris
    while outer is not None:
        level -= 1
        levels[level] = str(outer)
        outer = outer.outer_eris

    for level in sorted(levels.keys()):
        print('level', level)
        print(levels[level])


def main():
    colorama.init()

    eris = Eris()

    inputFile = basename(__file__)[:2] + '-input.txt'
    # inputFile = basename(__file__)[:2] + '-example-1.txt'

    y = 0
    with open(inputFile,  'r') as infile:
        for line in infile:
            for x, val in enumerate(line.rstrip()):
                pos = XY(x, y)
                if val == '#':
                    eris.set(pos, 1)
                else:
                    eris.set(pos, 0)
            y += 1

    for i in range(0, 200):
        print('minute', i + 1)
        eris.calculate_inner()
        eris.calculate_outer()

        inner = eris.inner_eris
        while inner is not None:
            inner.calculate_inner()
            inner.calculate_outer()
            inner = inner.inner_eris

        outer = eris.outer_eris
        while outer is not None:
            outer.calculate_inner()
            outer.calculate_outer()
            outer = outer.outer_eris

        eris.apply()
        inner = eris.inner_eris
        while inner is not None:
            inner.apply()
            inner = inner.inner_eris

        outer = eris.outer_eris
        while outer is not None:
            outer.apply()
            outer = outer.outer_eris

        # draw(eris)
        # print('-------------------------------')

    total_bugs = eris.bug_count()
    inner = eris.inner_eris
    while inner is not None:
        total_bugs += inner.bug_count()
        inner = inner.inner_eris
    outer = eris.outer_eris
    while outer is not None:
        total_bugs += outer.bug_count()
        outer = outer.outer_eris
    print(total_bugs)


if __name__ == "__main__":
    main()
