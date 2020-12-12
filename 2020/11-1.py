import argparse
import os


def main():
    day = os.path.basename(__file__).split('-')[0]
    challenge_input = '{}-input.txt'.format(day)
    # challenge_input = '{}-example.txt'.format(day)

    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default=challenge_input)
    args = parser.parse_args()

    lines = []
    with open(args.input, 'r') as infile:
        for line in infile:
            lines.append(line.strip())

    floorplan = Floorplan(lines)
    previously_occupied_positions = set()

    while True:
        new_occupied_positions = set()
        for pos in floorplan.seat_positions:
            occupied_adjacents = len(floorplan.get_adjacent_seats(pos) & previously_occupied_positions)
            if pos not in previously_occupied_positions and occupied_adjacents == 0:
                new_occupied_positions.add(pos)
            elif pos in previously_occupied_positions and occupied_adjacents < 4:
                new_occupied_positions.add(pos)
        if new_occupied_positions == previously_occupied_positions:
            print('Stabilised seat occupations:', len(new_occupied_positions))
            break
        previously_occupied_positions = new_occupied_positions


class Pos:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self._hash = y * 100 + x

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return '({},{})'.format(self.x, self.y)

    def __hash__(self):
        return self._hash


class Floorplan:
    def __init__(self, data: list[str]):
        self.seat_positions: set[Pos] = set()
        for x in range(len(data[0])):
            for y in range(len(data)):
                if data[y][x] == 'L':
                    self.seat_positions.add(Pos(x, y))

        self.adjacents = {}
        for seat_pos in self.seat_positions:
            seat_adjacents = set()
            for x in [seat_pos.x - 1, seat_pos.x, seat_pos.x + 1]:
                for y in [seat_pos.y - 1, seat_pos.y, seat_pos.y + 1]:
                    adjacent_pos = Pos(x, y)
                    if adjacent_pos != seat_pos and adjacent_pos in self.seat_positions:
                        seat_adjacents.add(adjacent_pos)
            self.adjacents[seat_pos] = seat_adjacents

    def get_adjacent_seats(self, pos):
        return self.adjacents[pos]


if __name__ == "__main__":
    main()
