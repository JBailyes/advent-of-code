from aocutils import load_input


def main():

    def sign(number:int) -> int:
        if number == 0:
            return 0
        if number > 0:
            return 1
        return -1


    class Pos():
        def __init__(self, x:int, y:int) -> None:
            self.x:int = x
            self.y:int = y
        
        def __eq__(self, __o: object) -> bool:
            return self.x == __o.x and self.y == __o.y
        
        def __str__(self) -> str:
            return f'{self.x},{self.y}'
        
        def up(self, distance:int =1):
            return Pos(self.x, self.y + distance)
        
        def down(self, distance:int =1):
            return Pos(self.x, self.y - distance)
        
        def left(self, distance:int =1):
            return Pos(self.x - distance, self.y)
        
        def right(self, distance:int =1):
            return Pos(self.x + distance, self.y)

        def touching(self, other) -> int:
            return abs(self.x - other.x) < 2 and abs(self.y - other.y) < 2

        def follow(self, other):
            x_diff: int = other.x - self.x
            y_diff: int = other.y - self.y
            # print('follow', self, other, x_diff, y_diff)
            new_x:int = self.x
            new_y:int = self.y

            diagonal = other.x != self.x and other.y != self.y
            if diagonal:
                new_x += sign(x_diff)
                new_y += sign(y_diff)
            else:
                if abs(x_diff) > 1:
                    new_x = self.x + sign(x_diff)
                if abs(y_diff) > 1:
                    new_y = self.y + sign(y_diff)

            return Pos(new_x, new_y)


    class Knot():
        def __init__(self, pos:Pos, next=None, record=False) -> None:
            self.pos:Pos = pos
            self.record:bool = record
            self.next_knot = next
            self.visited = set()
            self.visited.add(str(self.pos))

        def touching(self, other) -> int:
            return self.pos.touching(other.pos)
        
        def follow(self, other):
            if self.touching(other):
                return
            new_pos = self.pos.follow(other.pos)
            if new_pos != self.pos:
                self.pos = new_pos
                if self.record:
                    self.visited.add(str(self.pos))
                if self.next_knot:
                    self.next_knot.follow(self)
        
        def move(self, direction:str, amount:int):
            if direction == 'U':
                self.pos = self.pos.up(amount)
            elif direction == 'D':
                self.pos = self.pos.down(amount)
            elif direction == 'L':
                self.pos = self.pos.left(amount)
            elif direction == 'R':
                self.pos = self.pos.right(amount)
            
            if self.next_knot:
                self.next_knot.follow(self)
       
        def __str__(self) -> str:
            return str(self.pos)


    start = Pos(0,0)
    tail:Knot = Knot(start, record=True)
    knot_8:Knot = Knot(start, next=tail)
    knot_7:Knot = Knot(start, next=knot_8)
    knot_6:Knot = Knot(start, next=knot_7)
    knot_5:Knot = Knot(start, next=knot_6)
    knot_4:Knot = Knot(start, next=knot_5)
    knot_3:Knot = Knot(start, next=knot_4)
    knot_2:Knot = Knot(start, next=knot_3)
    knot_1:Knot = Knot(start, next=knot_2)
    head:Knot = Knot(start, next=knot_1)

    puzzle_input = load_input(__file__)
    # puzzle_input = load_input(__file__, 'example-2')

    for line in puzzle_input:
        direction, amount = line.split(' ')
        print(direction, amount)
        for _ in range(int(amount)):
            head.move(direction, 1)
            # print('H', head)
        # print(head, knot_1, knot_2, knot_3, knot_4, knot_5, knot_6, knot_7, knot_8, tail )


    print(head, tail)
    print(tail.visited)
    print('tail visited', len(tail.visited))

    # Correct answer: 2661


if __name__ == "__main__":
    main()
