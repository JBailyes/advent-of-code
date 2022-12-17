from aocutils import load_input
from copy import copy

def main():

    class Rock():
        def __init__(self, shape:str, x:int, y:int) -> None:
            if shape == '-':
                self.bits = [0b0011110]

            elif shape == '+':
                self.bits = [0b0001000,
                             0b0011100,
                             0b0001000]

            elif shape == 'L':
                self.bits = [0b0000100,
                             0b0000100,
                             0b0011100]

            elif shape == '|':
                self.bits = [0b0010000,
                             0b0010000,
                             0b0010000,
                             0b0010000]

            elif shape == '.':
                self.bits = [0b0011000,
                             0b0011000]

            self.bits.reverse()
            self.x = x
            self.y = y


    puzzle_input = load_input(__file__)
    puzzle_input = load_input(__file__, 'example')

    jet_moves = puzzle_input[0]

    chamber = []
    walls = 0b100000001

    rock_types = '-+L|.'
    rock:Rock = None
    last_rock_type:Rock = '.'
    settled = 0
    move_index = -1
    chamber_offest = 0
    # while settled < 1_000_000_000_000:
    while settled < 2022:
        if not rock:
            y = len(chamber) + 3
            x = 2
            next_type = rock_types[(rock_types.index(last_rock_type) + 1) % 5]
            last_rock_type = next_type
            rock = Rock(next_type, x, y)
        move_index = (move_index + 1) % len(jet_moves)
        move = jet_moves[move_index]

        shifted_rock = copy(rock.bits)
        for i, line in enumerate(shifted_rock):
            if move == '<':
                shifted_rock[i] = line << 1
            else:
                shifted_rock[i] = line >> 1

        blocked = False
        for i, shifted_line in enumerate(shifted_rock):
            if blocked:
                continue
            line_y = rock.y + i
            if shifted_line & walls != 0:
                blocked = True
            else:
                if line_y < len(chamber):
                    blocked |= chamber[line_y] & shifted_line != 0
        
        if not blocked:
            rock.bits = shifted_rock

        y_down = rock.y - 1

        blocked = False
        for i, line in enumerate(rock.bits):
            y_down = rock.y + i - 1
            blocked |= y_down == -1
            if -1 < y_down < len(chamber):
                blocked |= chamber[y_down] & line != 0
        if not blocked:
            rock.y -= 1
        else:
            for i, line in enumerate(rock.bits):
                y = rock.y + i
                if y >= len(chamber):
                    chamber.append(0)
                chamber[y] |= line
            settled += 1
            rock = None
            if settled % 1_000_000 == 0:
                print(settled, 'settled')
        
        # column_blocks = [0,0,0,0,0,0,0]
        # for x in range(7):
        #     blocked = False
        #     y = len(chamber)
        #     while not blocked and y > 1:
        #         y -= 1
        #         if chamber[y][x] == '#':
        #             blocked = True
        #             column_blocks[x] = y
        
        # block_min = min(column_blocks)
        # if block_min > 0:
        #     chamber = chamber[block_min:]
        #     chamber_offest += block_min
    
    
    # for line in reversed(chamber):
    #     print(f'|{line}|')#.replace(' ', '.'))
    # print('+-------+')
    # print()
    print('tower height', len(chamber) + chamber_offest)

    # Correct answer: 


if __name__ == "__main__":
    main()
