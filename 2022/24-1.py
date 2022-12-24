from aocutils import load_input


def main():

    puzzle_input = load_input(__file__)
    # puzzle_input = load_input(__file__, 'example')

    grid_width = len(puzzle_input[0]) - 2
    grid_height = len(puzzle_input) - 2

    class Pos():
        def __init__(self, x, y) -> None:
            self.x:int = x
            self.y:int = y
            self.coord_id:int = y * (grid_width + 2) + x
        
        def __str__(self) -> str:
            return f'({self.x},{self.y})'
        
        def __repr__(self) -> str:
            return self.__str__()

        def __hash__(self) -> int:
            return self.coord_id

        def __eq__(self, __o: object) -> bool:
            return __o is not None and self.coord_id == __o.coord_id

        def right(self):
            return Pos(self.x + 1, self.y)

        def left(self):
            return Pos(self.x - 1, self.y)

        def up(self):
            return Pos(self.x, self.y - 1)

        def down(self):
            return Pos(self.x, self.y + 1)

        def surrounding(self):
            return [self.up(), self.right(), self.down(), self.left()]


    class Blizzard():
        def __init__(self, p:Pos, direction:str) -> None:
            self.p = p
            self.direction = direction
            if direction == '>':
                self._blow = self._right
            elif direction == '<':
                self._blow = self._left
            elif direction == '^':
                self._blow = self._up
            elif direction == 'v':
                self._blow = self._down

        def _right(self):
            self.p = self.p.right()
            if self.p.x == grid_width:
                self.p = Pos(0, self.p.y)

        def _left(self):
            self.p = self.p.left()
            if self.p.x == -1:
                self.p = Pos(grid_width - 1, self.p.y)

        def _up(self):
            self.p = self.p.up()
            if self.p.y == -1:
                self.p = Pos(self.p.x, grid_height - 1)

        def _down(self):
            self.p = self.p.down()
            if self.p.y == grid_height:
                self.p = Pos(self.p.x, 0)

        def blow(self):
            self._blow()
            return self.p

        def __str__(self) -> str:
            return self.direction


    blizzards:list[Blizzard] = []
    valley_map:dict[Pos,list[Blizzard]] = {}

    for y, line in enumerate(puzzle_input[1:-1]):
        for x, c in enumerate(line[1:-1]):
            pos = Pos(x,y)
            valley_map[pos] = []
            if c != '.':
                blizzard = Blizzard(pos, c)
                blizzards.append(blizzard)
                valley_map[pos].append(blizzard)

    entrance:Pos = Pos(0,-1)
    way_out:Pos = Pos(grid_width - 1, grid_height)

    def print_valley(minute:int):
        print('Minute', minute)
        for y in range(grid_height):
            for x in range(grid_width):
                p = Pos(x,y)
                val = '.'
                blizz_list = valley_map[p]
                if len(blizz_list) > 1:
                    val = str(len(blizz_list))
                elif len(blizz_list) == 1:
                    val = blizz_list[0]
                else:
                    val = '.'
                print(val, end='')
            print()
        print()

    print_valley(0)


    def has_blizzards(p:Pos):
        return p in valley_map and len(valley_map[p]) > 0


    minute = 1
    routes:list[list[Pos]] = [[entrance]]
    while True:
        for blizzard in blizzards:
            valley_map[blizzard.p].remove(blizzard)
            valley_map[blizzard.blow()].append(blizzard)
        # print_valley(minute)

        new_routes:list[list[Pos]] = []
        for route in routes:
            expedition = route[-1]
            if not has_blizzards(expedition):
                new_routes.append(route)  # Stay put
            options = []
            for p in expedition.surrounding():
                if p == way_out:
                    print('Got to way out at minute', minute)
                    exit()
                elif p in valley_map and not has_blizzards(p):
                    options.append(p)

            for option in options:
                new_route = route + [option]
                # Only add this route if another one hasn't already got to this pos
                if option not in [r[-1] for r in new_routes]:
                    new_routes.append(new_route)

        routes = new_routes
        # for route in routes:
        #     print(route)
        # print()
        if minute % 100 == 0:
            print(f'{len(routes):,} routes')

        minute += 1
        
    # Correct answer: 253


if __name__ == "__main__":
    main()
