from aocutils import load_input
import re

def main():

    class P():
        def __init__(self, x, y, z=0) -> None:
            self.x:int = x
            self.z:int = z
            self.y:int = y
            self.coord_id:int = x * 2_500 + y * 50 + z
        
        def __str__(self) -> str:
            return f'[{self.x},{self.y}]'
        
        def __repr__(self) -> str:
            return self.__str__()

        def __hash__(self) -> int:
            return self.coord_id

        def __eq__(self, __o: object) -> bool:
            return __o is not None and self.coord_id == __o.coord_id

        def right(self):
            return P(self.x + 1, self.y)

        def left(self):
            return P(self.x - 1, self.y)

        def up(self):
            return P(self.x, self.y - 1)

        def down(self):
            return P(self.x, self.y + 1)

    
    class V(P):
        def rotate_in_x(self, clockwise=False):
            x = self.x
            cw = 1 if False else -1
            if clockwise:
                if self.z == 1:
                    return V(x, 1*cw, 0)
                if self.z == -1:
                    return V(x, -1*cw, 0)
                if self.y == 1:
                    return V(x, 0, -1*cw)
                if self.y == -1:
                    return V(x, 0, 1*cw)

        def rotate_in_y(self, clockwise=False):
            y = self.y
            cw = 1 if False else -1
            if self.z == 1:
                return V(-1*cw, y, 0)
            if self.z == -1:
                return V(1*cw, y, 0)
            if self.x == 1:
                return V(0, y, 1*cw)
            if self.x == -1:
                return V(0, y, -1*cw)

        def rotate_in_z(self, clockwise=False):
            z = self.z
            cw = 1 if False else -1
            if self.x == 1:
                return V(0, 1*cw, z)
            if self.x == -1:
                return V(0, -1*cw, z)
            if self.y == 1:
                return V(-1*cw, 0, z)
            if self.y == -1:
                return V(1*cw, 0, z)
    

    class Tile():
        def __init__(self, pos:P, orientation:V, x_direction:V, y_direction:V) -> None:
            self.o:V = orientation
            self.p:P = pos
            self.xd:V = x_direction
            self.yd:V = y_direction


    puzzle_input = load_input(__file__)
    cube_size:int = 50
    puzzle_input = load_input(__file__, 'example')
    cube_size:int = 4

    instructions = puzzle_input[-1]
    tiles:list[str] = puzzle_input[0:-2]

    width = max([len(row) for row in tiles])
    for i, row in enumerate(tiles):
        if len(row) < width:
            tiles[i] = row + ' ' * (width - len(row))

    mapped_tiles:dict[P,Tile] = {}

    for top_start in range(len(tiles), step=cube_size):
        unmapped = [P(side_start, top_start) for side_start in range(0, width, step=cube_size)]
        while unmapped:
            for left_start in range(0, width, step=cube_size):
                top_left = P(left_start, top_start)
                top_right = P(left_start + cube_size - 1, top_start)

                if tiles[top_left.y][top_left.x] == ' ':
                    unmapped.remove(top_left)
                    continue

                if len(mapped_tiles) == 0:  # This is our starting side
                    o = V(0,0,1)
                    xd = V(1,0,0)
                    yd = V(0,1,0)
                
                # Look for mapped tiles around this one, to determine its orientation
                elif top_left.up() in mapped_tiles:
                    o = mapped_tiles[top_left.up()].o.rotate_in_x()
                    f = mapped_tiles[top_left.up()].f.rotate_in_x()
                elif top_left.left() in mapped_tiles:
                    o = mapped_tiles[top_left.left()].o.rotate_in_z()
                    f = mapped_tiles[top_left.left()].f.rotate_in_z()
                elif top_right.right() in mapped_tiles:
                    o = mapped_tiles[top_right.right()].o.rotate_in_z(clockwise=True)
                    f = mapped_tiles[top_right.right()].f.rotate_in_z(clockwise=True)
                else:
                    unmapped.remove(top_left)
                    continue

                for x in range(cube_size):
                    for y in range(cube_size):
                        flat_pos = P(left_start + x, top_start + y)
                        value = tiles[top_start + y][left_start + x]
                        



    # class Edge():
    #     def __init__(self, re_face, re_pos) -> None:
    #         self._re_pos = re_pos
    #         self._re_face = re_face
        
    #     def re_pos(self, pos):
    #         return self._re_pos(pos)
        
    #     def re_face(self, facing) -> int:
    #         return (facing + self._re_face) % 4


    # transitions = []
    # for y in range(len(tiles)):
    #     transitions.append([])
    #     for x in range(width):
    #         transitions.append(None)

    # for x in range(cube_size * 2, cube_size * 3):
    #     y = 0
    #     transitions[y][x] = Edge(2, lambda pos: 
    #         Pos(cube_size - (pos.x - cube_size*2), pos.y - cube_size))

    # for y in range(cube_size):
    #     x = cube_size * 2
    #     transitions[y][x] = Edge(-1, lambda pos: 
    #         Pos(y + cube_size, y))
            
    #     x += cube_size - 1
    #     transitions[y][x] = Edge(2, lambda pos: 
    #         Pos(x + cube_size, (cube_size - y) + cube_size*2))


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
