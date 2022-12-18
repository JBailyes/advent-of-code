from aocutils import load_input


def main():

    class Pos():
        def __init__(self, x, y, z) -> None:
            self.x:int = x
            self.y:int = y
            self.z:int = z
            self.coord_id:int = x * 10_000 + y * 100 + z
        
        def __str__(self) -> str:
            return f'[{self.x},{self.y},{self.z}]'
        
        def __repr__(self) -> str:
            return self.__str__()

        def __hash__(self) -> int:
            return self.coord_id

        def __eq__(self, __o: object) -> bool:
            return __o is not None and self.coord_id == __o.coord_id

        def right(self):
            return Pos(self.x + 1, self.y, self.z)

        def left(self):
            return Pos(self.x - 1, self.y, self.z)

        def up(self):
            return Pos(self.x, self.y - 1, self.z)

        def down(self):
            return Pos(self.x, self.y + 1, self.z)
            
        def towards(self):
            return Pos(self.x, self.y, self.z + 1)

        def away(self):
            return Pos(self.x, self.y, self.z - 1)
        


    puzzle_input = load_input(__file__)
    # puzzle_input = load_input(__file__, 'example')

    droplets:set[Pos] = set()

    for line in puzzle_input:
        x, y, z = (int(n) for n in line.split(','))
        print(x,y,z)
        droplets.add(Pos(x,y,z))
    
    unconnected = 0
    for droplet in droplets:
        for surrounding_pos in (droplet.left(), droplet.right(),
                                droplet.up(), droplet.down(),
                                droplet.away(), droplet.towards()):
            if surrounding_pos not in droplets:
                unconnected += 1
    print(unconnected)

    # Correct answer: 3564


if __name__ == "__main__":
    main()
