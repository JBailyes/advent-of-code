from aocutils import load_input


def main():

    class Rock():
        def __init__(self, shape:str, x:int, y:int) -> None:
            if shape == '-':
                self.bits = ['####']

            elif shape == '+':
                self.bits = [' # ',
                             '###',
                             ' # ']

            elif shape == 'L':
                self.bits = ['  #',
                             '  #',
                             '###']

            elif shape == '|':
                self.bits = ['#',
                             '#',
                             '#',
                             '#']

            elif shape == '.':
                self.bits = ['##',
                             '##']

            self.bits.reverse()
            self.x = x
            self.y = y


    puzzle_input = load_input(__file__)
    # puzzle_input = load_input(__file__, 'example')

    jet_moves = puzzle_input[0]

    chamber = []

    rock_types = '-+L|.'
    rock:Rock = None
    last_rock_type:Rock = '.'
    settled = 0
    move_index = -1
    while settled < 2022:
        if not rock:
            y = len(chamber) + 3
            x = 2
            next_type = rock_types[(rock_types.index(last_rock_type) + 1) % 5]
            last_rock_type = next_type
            # print('new rock type', next_type, 'at', x, y)
            rock = Rock(next_type, x, y)
        move_index = (move_index + 1) % len(jet_moves)
        move = jet_moves[move_index]
        if move == '<':
            blocked = False
            for i, line in enumerate(rock.bits):
                leftmost = rock.x + line.index('#')
                line_y = rock.y + i
                if leftmost - 1 == -1:
                    blocked = True
                elif line_y < len(chamber):
                    blocked |= chamber[line_y][leftmost - 1] == '#'
            if not blocked:
                rock.x -= 1
        if move == '>':
            blocked = False
            for i, line in enumerate(rock.bits):
                rightmost = rock.x + line.rindex('#')
                line_y = rock.y + i
                if rightmost + 1 == 7:
                    blocked = True
                elif line_y < len(chamber):
                    blocked |= chamber[line_y][rightmost + 1] == '#'
            if not blocked:
                rock.x += 1

        y_down = rock.y - 1

        blocked = False
        for i, line in enumerate(rock.bits):
            y_down = rock.y + i - 1
            blocked |= y_down == -1
            if -1 < y_down < len(chamber):
                for j, material in enumerate(line):
                    if material == '#':
                        blocked |= chamber[y_down][rock.x + j] == '#'
        if not blocked:
            rock.y -= 1
        else:
            for i, line in enumerate(rock.bits):
                y = rock.y + i
                if y >= len(chamber):
                    chamber.append('       ')
                new_chamber_line = [char for char in chamber[y]]
                for j, material in enumerate(line):
                    if material == '#':
                        new_chamber_line[rock.x + j] = '#'
                chamber[y] = ''.join(new_chamber_line)
            settled += 1
            rock = None
        
        # for line in reversed(chamber):
        #     print(f'|{line}|')#.replace(' ', '.'))
        # print('+-------+')
        # print()
    
    
    for line in reversed(chamber):
        print(f'|{line}|')#.replace(' ', '.'))
    print('+-------+')
    print()
    print('tower height', len(chamber))

    # Correct answer: 3197


if __name__ == "__main__":
    main()
