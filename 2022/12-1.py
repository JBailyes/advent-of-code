import string
from aocutils import load_input


def main():


    puzzle_input = load_input(__file__)
    # puzzle_input = load_input(__file__, 'example')

    grid_width = len(puzzle_input[0])
    grid_height = len(puzzle_input)

    class Pos():
        def __init__(self, x, y) -> None:
            self.x:int = x
            self.y:int = y
            self.coord_id:int = x * grid_width + y
        
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

        def in_grid(self):
            return (0 <= self.x < grid_width) and (0 <= self.y < grid_height)


    grid:dict[Pos,int] = {}
    start:Pos = None
    signal:Pos = None

    for y, line in enumerate(puzzle_input):
        for x, letter in enumerate(line):
            pos = Pos(x, y)
            if letter == 'S':
                start = pos
                height = 0
            elif letter == 'E':
                signal = pos
                height = 25
            else:
                height = string.ascii_lowercase.index(letter)
            grid[pos] = height
            print(f'{str(pos):>7}{height:>2}  ', end='')
        print()


    def options(path:list[Pos]) -> list[Pos]:
        head:Pos = path[-1]
        prev:Pos = None
        if len(path) > 1:
            prev = path[-2]
        
        up = head.up()
        down = head.down()
        left = head.left()
        right = head.right()

        return [pos for pos in [up, down, left, right] if pos.in_grid() and pos != prev and grid[pos] <= grid[head] + 1]


    def find_shortest() -> list[Pos]:
        paths:list[list[Pos]] = []
        paths.append([start])
        discarded_paths:list[list[Pos]] = []
        visited:set[Pos] = set()
        
        while True:
            new_paths:list[list[Pos]] = []
            for path in paths:
                for next_pos in options(path):
                    new_paths.append(path + [next_pos])
                discarded_paths.append(path)

            paths = []
            for new_path in new_paths:
                head = new_path[-1]

                # Each path up to now has progressed on step at a time together, so the first to
                # arrive at Signal is the shortest or joint shortest
                if head == signal:
                    return new_path

                # Don't continue this path if we already got to this pos in a shorter or equivalent path
                if not head in visited:
                    visited.add(head)
                    paths.append(new_path)
            print(f'Progressing {len(paths)} paths')


    shortest:list[Pos] = find_shortest()
    print(len(shortest) - 1)  

    # Correct answer: 484


if __name__ == "__main__":
    main()
