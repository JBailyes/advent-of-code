from aocutils import load_input


def main():
    puzzle_input = load_input(__file__)
    # puzzle_input = load_input(__file__, 'example')
    
    class Pos():
        def __init__(self, x, y) -> None:
            self.x:int = x
            self.y:int = y
            self.pos_id:int = x * 1_000 + y
        
        def __str__(self) -> str:
            return f'[{self.x},{self.y}]'
        
        def __repr__(self) -> str:
            return self.__str__()

        def __hash__(self) -> int:
            return self.pos_id

        def __eq__(self, __o: object) -> bool:
            return __o is not None and self.pos_id == __o.pos_id

        def down_left(self):
            return Pos(self.x - 1, self.y + 1)

        def down_right(self):
            return Pos(self.x + 1, self.y + 1)

        def down(self):
            return Pos(self.x, self.y + 1)


    map:dict[Pos,str] = {}

    for line in puzzle_input:
        last_pos:Pos = None
        for pos_str in line.split(' -> '):
            x, y = [int(c) for c in pos_str.split(',')]
            pos = Pos(x,y)
            if last_pos:
                x_diff = abs(pos.x - last_pos.x)
                y_diff = abs(pos.y - last_pos.y)
                start_x = min(last_pos.x, pos.x)
                start_y = min(last_pos.y, pos.y)
                for x in range(start_x, start_x + x_diff + 1):
                    for y in range(start_y, start_y + y_diff + 1):
                        rock_pos = Pos(x,y)
                        map[rock_pos] = '#'
            last_pos = pos
    
    max_rock_y = max([pos.y for pos in map.keys()])
    source = Pos(500,0)
    settled_sand:set[Pos] = set()

    freefall = False
    while not freefall:
        grain_pos = source
        settling = True
        while settling and not freefall:
            if not grain_pos.down() in map:
                grain_pos = grain_pos.down()
            elif not grain_pos.down_left() in map:
                grain_pos = grain_pos.down_left()
            elif not grain_pos.down_right() in map:
                grain_pos = grain_pos.down_right()
            else:
                map[grain_pos] = 'o'
                settled_sand.add(grain_pos)
                settling = False
            freefall = grain_pos.y > max_rock_y
    
    # print(map)
    print(len(settled_sand))

    # Correct answer: 1001


if __name__ == "__main__":
    main()
