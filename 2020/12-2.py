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

    ferry = Ferry()
    for instruction in lines:
        ferry.act(Instruction(instruction))

    m_dist = abs(ferry.pos.x) + abs(ferry.pos.y)
    print('Ending coords:', ferry.pos)
    print('Manhattan distance:', m_dist)


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


class Instruction:
    def __init__(self, instruction: str):
        self.action = instruction[0]
        self.value = int(instruction[1:])


class Ferry:
    def __init__(self):
        self.pos = Pos(0, 0)
        self.waypoint = Pos(10, 1)

    def act(self, instruction: Instruction):
        action: str = instruction.action
        value: int = instruction.value

        compass = 'NESW'
        vectors = {
            'N': Pos(0, 1),
            'E': Pos(1, 0),
            'S': Pos(0, -1),
            'W': Pos(-1, 0),
        }

        if action in compass:
            self.waypoint.x += vectors[action].x * value
            self.waypoint.y += vectors[action].y * value
        elif action == 'F':
            self.pos.x += self.waypoint.x * value
            self.pos.y += self.waypoint.y * value
        elif action in 'LR':
            if action == 'L':
                value = 360 - value
            x = self.waypoint.x
            y = self.waypoint.y
            if value == 90:
                self.waypoint = Pos(y, -x)
            elif value == 180:
                self.waypoint = Pos(-x, -y)
            elif value == 270:
                self.waypoint = Pos(-y, x)


if __name__ == "__main__":
    main()
