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

        def get_surrounding(self):
            return set((self.left(), self.right(),
                        self.up(), self.down(),
                        self.away(), self.towards()))
        


    puzzle_input = load_input(__file__)
    # puzzle_input = load_input(__file__, 'example')

    droplets:set[Pos] = set()

    x_vals = set()
    y_vals = set()
    z_vals = set()

    for line in puzzle_input:
        x, y, z = (int(n) for n in line.split(','))
        # print(x,y,z)
        x_vals.add(x)
        y_vals.add(y)
        z_vals.add(z)
        droplets.add(Pos(x,y,z))

    min_x = min(x_vals)
    max_x = max(x_vals)
    min_y = min(y_vals)
    max_y = max(y_vals)
    min_z = min(z_vals)
    max_z = max(z_vals)

    print(min_x, max_x, min_y, max_y, min_z, max_z)


    def is_external_pos(p:Pos):
        return p.x < min_x or p.x > max_x or p.y < min_y or p.y > max_y or p.z < min_z or p.z > max_z


    external_air:set[Pos] = set()
    low_x = min_x - 1
    high_x = max_x + 1
    while low_x < high_x:
        low_y = min_y - 1
        high_y = max_y + 1
        while low_y < high_y:
            low_z = min_z - 1
            high_z = max_z + 1
            while low_z < high_z:
                for x in range(low_x, high_x + 1):
                    for y in range(low_y, high_y + 1):
                        for z in range(low_z, high_z + 1):
                            pos = Pos(x,y,z)
                            if pos not in droplets:
                                if is_external_pos(pos):
                                    external_air.add(pos)
                                else:
                                    for surrounding in pos.get_surrounding():
                                        if surrounding in external_air:
                                            external_air.add(pos)
                low_z += 1
                high_z -= 1
            low_y += 1
            high_y -=1
        low_x += 1
        high_x -= 1

    
    external_air_area = 0
    for droplet in droplets:
        for surrounding_pos in droplet.get_surrounding():
            if surrounding_pos in external_air:
                external_air_area += 1
    print('air area', external_air_area)

    with open('18-output.txt', 'w') as outfile:
        for z in range(min_z, max_z + 1):
            outfile.write('+' + ('-' * (max_x - min_x + 1)) + '+\n')
            for y in range(min_y, max_y + 1):
                outfile.write('|')
                for x in range(min_x, max_x + 1):
                    pos = Pos(x,y,z)
                    if pos in external_air:
                        outfile.write('.')
                    else:
                        outfile.write('#' if pos in droplets else ' ')
                outfile.write('|\n')
            outfile.write('+' + ('-' * (max_x - min_x + 1)) + '+\n')
            outfile.write('\n')

    # Wrong: 3408, 1626, 2101
    # Correct answer: 2106


if __name__ == "__main__":
    main()
