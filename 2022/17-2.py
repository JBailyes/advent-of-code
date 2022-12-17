from aocutils import load_input
from copy import copy

def main():

    class Rock():
        def __init__(self, shape:str, y:int) -> None:
            if shape == '-':
                self.bits = [0b000111100]

            elif shape == '+':
                self.bits = [0b000010000,
                             0b000111000,
                             0b000010000]

            elif shape == 'L':
                self.bits = [0b000001000,
                             0b000001000,
                             0b000111000]

            elif shape == '|':
                self.bits = [0b000100000,
                             0b000100000,
                             0b000100000,
                             0b000100000]

            elif shape == '.':
                self.bits = [0b000110000,
                             0b000110000]

            self.bits.reverse()
            self.y = y


    puzzle_input = load_input(__file__)
    # puzzle_input = load_input(__file__, 'example')

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
    # while settled < 2022:

    # Manual analysis after running to 10,000 settled:
    # Pettern emerges at 2,335
    # Pattern is 2,690 lines
    # Outputting on boundaries of pattern shows consistent rock settle of 1,715 per repeat of pattern
    # Settled rocks at start of first pattern is 1,475
    # Move index 8,440
    # 
    # (1_000_000_000_000 - 1_475) % 1_715 == 255

    pattern_start = 2_335
    pattern_size = 2_690
    pattern_repeats = int((1_000_000_000_000 - 1_475) / 1_715)
    settled = 1_000_000_000_000 - 255
    move_index = 8_439
    chamber_offset = pattern_start + pattern_repeats * pattern_size

    while settled < 1_000_000_000_000:
    # while settled < 2022:
    # while settled < 10_000:
        if not rock:
            y = len(chamber) + 3
            next_type = rock_types[(rock_types.index(last_rock_type) + 1) % 5]
            last_rock_type = next_type
            rock = Rock(next_type, y)
        move_index = (move_index + 1) % len(jet_moves)
        move = jet_moves[move_index]

        shifted_rock = copy(rock.bits)
        for i, line in enumerate(shifted_rock):
            shifted_rock[i] = line << 1 if move == '<' else line >> 1

        blocked = False
        for i, shifted_line in enumerate(shifted_rock):
            if blocked:
                continue
            line_y = rock.y + i
            if line_y < len(chamber):
                blocked |= chamber[line_y] & shifted_line != 0
            else:
                blocked |= shifted_line & walls != 0
        
        if not blocked:
            rock.bits = shifted_rock

        # for line in rock.bits:
        #     print(f'{line:09b}'.replace('0', ' '))
        # print()

        blocked = False
        for i, line in enumerate(rock.bits):
            y_down = rock.y + i - 1
            blocked |= y_down == -1
            if -1 < y_down < len(chamber):
                blocked |= chamber[y_down] & line != 0
        if not blocked:
            rock.y -= 1
        else:
            chamber_min = 0
            for i, line in enumerate(rock.bits):
                y = rock.y + i
                if y >= len(chamber):
                    chamber.append(walls)
                chamber[y] |= line
                if chamber[y] == 0b111111111:
                    chamber_min = y
            settled += 1
            rock = None
            # if chamber_min:
            #     chamber = chamber[chamber_min:]
            #     chamber_offset += chamber_min
            if settled % 1_000_000 == 0:
                print(settled, 'settled')
            if (len(chamber) - 2335) % 2690 == 0:
            # if len(chamber) % 2690 == 0:
                print('line', len(chamber), 'settled rocks', settled, 'move index', move_index)
    
    
    with open('17-output.txt', 'w') as outfile:
        for line in reversed(chamber):
            display = '|' + f'{line:09b}'[1:-1].replace('0', ' ').replace('1', '*') + '|'
            # print(display)
            outfile.write(display + '\n')
    print('+-------+')
    print()
    print('tower height', len(chamber) + chamber_offset)

    # 1568513119574 is too high
    # 1568513119573 is too high
    # Correct answer: 


if __name__ == "__main__":
    main()
