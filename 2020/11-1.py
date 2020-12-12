import argparse
import os


def main():
    day = os.path.basename(__file__).split('-')[0]
    challenge_input = '{}-input.txt'.format(day)
    # challenge_input = '{}-example-1.txt'.format(day)
    # challenge_input = '{}-example-2.txt'.format(day)

    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default=challenge_input)
    args = parser.parse_args()

    lines = []
    with open(args.input, 'r') as infile:
        for line in infile:
            lines.append(line.strip())


class Floorplan:
    def __init__(self, data: list[str]):
        self.plan = {}
        for x in range(len(data[0])):
            for y in range(len(data)):
                if data[y][x] == 'L':
                    self.add_seat(x, y)

    def add_seat(self, x: int, y: int):
        pos = Pos(x, y)
        self.plan[pos] = Seat(pos)

    def analyse_layout(self):
        for seat in self.plan:
            for x in range(seat.x - 1, seat.x + 1):
                for y in range(seat.y - 1, seat.y + 1):
                    pos = Pos(x, y)
                    if pos != seat.pos and pos in self.plan.keys():
                        seat.add_adjacent(self.plan[pos])
        

class Pos:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return '({},{})'.format(self.x, self.y)


class Seat:
    def __init__(self, pos: Pos):
        self.occupied: bool = False
        self.position = pos
        self.adjacent_seats = set()

    def add_adjacent(self, seat):
        self.adjacent_seats.add(seat)


if __name__ == "__main__":
    main()
