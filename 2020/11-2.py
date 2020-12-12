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
            elif pos in previously_occupied_positions and occupied_adjacents < 5:
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
        self.max_x = len(data[0]) - 1
        self.max_y = len(data) - 1
        self.seat_positions: set[Pos] = set()
        for x in range(len(data[0])):
            for y in range(len(data)):
                if data[y][x] == 'L':
                    self.seat_positions.add(Pos(x, y))

        self.lines_of_sight = {}
        for seat_pos in self.seat_positions:
            visibles = set()
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    x = seat_pos.x
                    y = seat_pos.y
                    seat_seen = False
                    while 0 <= x <= self.max_x and 0 <= y <= self.max_y and not seat_seen:
                        x += dx
                        y += dy
                        visible_pos = Pos(x, y)
                        if visible_pos in self.seat_positions:
                            visibles.add(visible_pos)
                            seat_seen = True
            self.lines_of_sight[seat_pos] = visibles

    def get_adjacent_seats(self, pos):
        return self.lines_of_sight[pos]


if __name__ == "__main__":
    main()
