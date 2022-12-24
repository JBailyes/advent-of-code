from aocutils import load_input


def main():

    class Pos():
        def __init__(self, x, y) -> None:
            self.x:int = x
            self.y:int = y
            self.coord_id:int = y * 100_000 + x
        
        def __str__(self) -> str:
            return f'[{self.x},{self.y}]'
        
        def __repr__(self) -> str:
            return self.__str__()

        def __hash__(self) -> int:
            return self.coord_id

        def __eq__(self, __o: object) -> bool:
            return __o is not None and self.coord_id == __o.coord_id

        def e(self):
            return Pos(self.x + 1, self.y)

        def w(self):
            return Pos(self.x - 1, self.y)

        def n(self):
            return Pos(self.x, self.y - 1)

        def s(self):
            return Pos(self.x, self.y + 1)

        def ne(self):
            return Pos(self.x + 1, self.y - 1)

        def nw(self):
            return Pos(self.x -1, self.y - 1)

        def se(self):
            return Pos(self.x + 1, self.y + 1)

        def sw(self):
            return Pos(self.x - 1, self.y + 1)

    
    class Elf():
        def __init__(self, pos:Pos) -> None:
            self.pos = pos

    
    def get_propose_order(round:int):
        shift = round % 4
        check = 'nswe'
        return check[shift:] + check[0:shift]


    elves:dict[Pos,Elf] = {}


    puzzle_input = load_input(__file__)
    # puzzle_input = load_input(__file__, 'example')

    for y, line in enumerate(puzzle_input):
        for x, val in enumerate(line):
            if val == '#':
                pos = Pos(x,y)
                elves[pos] = Elf(pos)

    round = 0
    while True:
        if round % 100 == 0:
            print('Round', round + 1)
        propositions:dict[Pos,list[Elf]] = {}
        directions = get_propose_order(round)

        for pos, elf in elves.items():

            n = pos.n()
            s = pos.s()
            w = pos.w()
            e = pos.e()
            ne = pos.ne()
            nw = pos.nw()
            se = pos.se()
            sw = pos.sw()

            if not any([p in elves for p in [n,e,w,s,ne,nw,se,sw]]):
                continue

            proposed = False
            for direction in directions:
                if proposed:
                    continue
                if direction == 'n':
                    prop_pos = n
                    check = [n, ne, nw]
                elif direction == 's':
                    prop_pos = s
                    check = [s, se, sw]
                elif direction == 'w':
                    prop_pos = w
                    check = [w, nw, sw]
                elif direction == 'e':
                    prop_pos = e
                    check = [e, ne, se]
                free = not any([p in elves for p in check])
                if free:
                    propositions.setdefault(prop_pos, []).append(elf)
                    proposed = True
        
        moves = 0
        for new_pos, elf_list in propositions.items():
            if len(elf_list) == 1:
                elf:Elf = elf_list[0]
                del elves[elf.pos]
                elves[new_pos] = elf
                elf.pos = new_pos
                moves += 1
        
        if moves == 0:
            print('No moves in round', round + 1)
            exit()
        
        round += 1

    # Correct answer: 950


if __name__ == "__main__":
    main()
