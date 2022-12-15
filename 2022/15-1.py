from aocutils import load_input

import re


def main():
    puzzle_input = load_input(__file__)
    # puzzle_input = load_input(__file__, 'example')

    
    class Pos():
        def __init__(self, x, y) -> None:
            self.x:int = x
            self.y:int = y
            self.str:str = f'[{x},{y}]'
            self.hash:int = self.str.__hash__()
        
        def __str__(self) -> str:
            return self.str
        
        def __repr__(self) -> str:
            return self.__str__()

        def __hash__(self) -> int:
            return self.hash

        def __eq__(self, __o: object) -> bool:
            return __o is not None and self.hash == __o.hash


    def manhattan(p1:Pos, p2:Pos) -> int:
        return abs(p1.x - p2.x) + abs(p1.y - p2.y)


    beaconless:set[Pos] = set()

    row_of_interest = 2_000_000
    # row_of_interest = 10

    for line in puzzle_input:
        match = re.match(r'.*x=(-?\d+), y=(-?\d+).*x=(-?\d+), y=(-?\d+)', line)
        sensor:Pos = Pos(int(match.group(1)), int(match.group(2)))
        beacon:Pos = Pos(int(match.group(3)), int(match.group(4)))

        distance = manhattan(sensor, beacon)

        # Only relevant if its area goes over the line of interest
        if not (sensor.y - distance <= row_of_interest <= sensor.y + distance):
            continue

        x_diff = distance - abs(sensor.y - row_of_interest)
        # for x in range(sensor.x - distance, sensor.x + distance + 1):
            # for y in range(sensor.y - distance, sensor.y + distance + 1):
                # p = Pos(x,y)
                # if p != beacon and manhattan(sensor, p) <= distance:
                #     beaconless.add(p)
        for x in range(sensor.x - x_diff, sensor.x + x_diff + 1):
            p = Pos(x, row_of_interest)
            if p != beacon:
                beaconless.add(p)

    print(len([pos for pos in beaconless if pos.y == row_of_interest]))


    # Correct answer: 5525847


if __name__ == "__main__":
    main()
