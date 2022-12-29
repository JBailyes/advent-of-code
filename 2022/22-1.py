from aocutils import load_input
import re

def main():

    class Pos():
        def __init__(self, x, y) -> None:
            self.x:int = x
            self.y:int = y
            self.coord_id:int = x * 6000 + y
        
        def __str__(self) -> str:
            return f'[{self.x},{self.y}]'
        
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
    

    puzzle_input = load_input(__file__)
    # puzzle_input = load_input(__file__, 'example')

    instructions = puzzle_input[-1]
    tiles:list[str] = puzzle_input[0:-2]

    width = max([len(row) for row in tiles])
    for i, row in enumerate(tiles):
        if len(row) < width:
            tiles[i] = row + ' ' * (width - len(row))


    compass = ['>', 'v', '<', '^']

    pos:Pos = Pos(tiles[0].index('.'), 0)
    facing:int = 0
    print(pos, compass[facing])

    
    for inst_match in re.finditer(r'\d+|L|R', instructions):
        instruction = inst_match.group()
        print(instruction)
        if instruction == 'L':
            facing = (facing - 1) % 4
            print(pos, compass[facing])
        elif instruction == 'R':
            facing = (facing + 1) % 4
            print(pos, compass[facing])
        else:
            move = int(instruction)
            for _ in range(move):
                if compass[facing] == '>':
                    next = pos.right()
                elif compass[facing] == 'v':
                    next = pos.down()
                elif compass[facing] == '<':
                    next = pos.left()
                elif compass[facing] == '^':
                    next = pos.up()
                
                if compass[facing] in '<>':
                    row:str = tiles[next.y]
                    first_x:int = row.index('.')
                    last_x:int = row.rindex('.')
                    if '#' in row:
                        first_x = min(first_x, row.index('#'))
                        last_x = max(last_x, row.rindex('#'))

                    if next.x < first_x:
                        next = Pos(last_x, next.y)
                    elif next.x > last_x:
                        next = Pos(first_x, next.y)

                elif compass[facing] in '^v':
                    column:str = ''.join([row[next.x] for row in tiles])
                    first_y:int = column.index('.')
                    last_y:int = column.rindex('.')
                    if '#' in column:
                        first_y = min(first_y, column.index('#'))
                        last_y = max(last_y, column.rindex('#'))

                    if next.y < first_y:
                        next = Pos(next.x, last_y)
                    elif next.y > last_y:
                        next = Pos(next.x, first_y)
                
                if tiles[next.y][next.x] == '.':
                    pos = next
                    print(pos)

    print(pos)
    print((pos.y + 1) * 1000 + (pos.x + 1) * 4 + facing)
    
    # Correct answer: 149138


if __name__ == "__main__":
    main()
