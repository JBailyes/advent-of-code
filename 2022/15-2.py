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

    
    class Range():
        def __init__(self, start, end) -> None:
            self.start:int = start
            self.end:int = end
            self.str:str = f'{start} to {end}'

        def get_start(self) -> int:
            return self.start
        
        def __str__(self) -> str:
            return self.str
    

    class Area():
        def __init__(self, sensor:Pos, distance:int) -> None:
            self.sensor:Pos = sensor
            self.distance:int = distance
            self.top:int = sensor.y - distance
            self.bottom:int = sensor.y + distance
            self.left:int = sensor.x - distance
            self.right:int = sensor.x + distance
        
        def intersection(self, row:int, max_index:int) -> list[Range] | None:
            if not self.top <= row <= self.bottom:
                return None
            x_dist:int = self.distance - abs(row - self.sensor.y)
            x_left = self.sensor.x - x_dist
            x_right = self.sensor.x + x_dist

            if not (x_right >= 0 and x_left <= max_index):
                return None
            return Range(x_left, x_right)
        
        def __str__(self) -> str:
            return f'Area[sensor={self.sensor}, top={self.top}, bottom={self.bottom}, left={self.left}, right={self.right}]'


    box_max = 4_000_000
    # box_max = 20

    scans:list[Area] = []

    for line in puzzle_input:
        match = re.match(r'.*x=(-?\d+), y=(-?\d+).*x=(-?\d+), y=(-?\d+)', line)
        sensor:Pos = Pos(int(match.group(1)), int(match.group(2)))
        beacon:Pos = Pos(int(match.group(3)), int(match.group(4)))

        distance = manhattan(sensor, beacon)
        scans.append(Area(sensor, distance))


    def answer(x:int, y:int):
        tuning_freq = x * 4_000_000 + y
        print(f'x:{x}, y:{y} : {tuning_freq}')
        exit()


    for y in range(0, box_max + 1):
        intersections:list[Range] = []
        for area in scans:
            intersection:Range = area.intersection(y, box_max)
            if intersection:
                # print(area)
                intersections.append(intersection)
        intersections.sort(key=Range.get_start)
        start_x = intersections[0].start
        end_x = intersections[0].end
        if start_x > 0:
            answer(0, y)
        for intersection in intersections:
            # print(intersection)
            if intersection.start > end_x + 1:
                answer(end_x + 1, y)
            end_x = max(end_x, intersection.end)

    # Correct answer: 13340867187704


if __name__ == "__main__":
    main()
