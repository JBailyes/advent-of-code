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


    chamber = []
    walls = 0b100000001

    rock_types = '-+L|.'
    rock:Rock = None
    last_rock_type:Rock = '.'
    settled = 0
    move_index = -1
    chamber_offset = 0
    # while settled < 1_000_000_000_000:
    # while settled < 2022:

    # Manual analysis after running to 10,000 settled:
    # Pettern emerges after 2,335
    # Pattern is 2,690 lines
    # Outputting on boundaries of pattern shows consistent rock settle of 1,715 per repeat of pattern
    # Settled rocks just before start of first pattern is 1,475
    # Move index just before start of first pattern is 8,440

    # # My input:
    puzzle_input = load_input(__file__)
    outfile_name = '17-output.txt'
    last_line_before_pattern = 2_335
    pattern_size_lines = 2_690
    move_index = 8_440
    pattern_emerge_settled = 1_475
    settle_per_pattern = 1_715

    # # Example input
    # puzzle_input = load_input(__file__, 'example')
    # outfile_name = '17-output-example.txt'
    # last_line_before_pattern = 95
    # pattern_size_lines = 212
    # move_index = 14
    # pattern_emerge_settled = 59
    # settle_per_pattern = 140

    jet_moves = puzzle_input[0]

    pattern_repeats = int((1_000_000_000_000 - pattern_emerge_settled) / settle_per_pattern)
    rocks_left_to_settle = (1_000_000_000_000 - pattern_emerge_settled) % settle_per_pattern
    settled = 1_000_000_000_000 - rocks_left_to_settle
    chamber_offset = last_line_before_pattern + pattern_repeats * pattern_size_lines

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
                    chamber.append(walls)
                chamber[y] |= line
                if (len(chamber) - last_line_before_pattern) % pattern_size_lines == 0:
                    display = '|' + f'{chamber[y]:09b}'[1:-1].replace('0', ' ').replace('1', '*') + '|'
                    print(display, ', line', len(chamber), ', settled rocks', settled, ', move index', move_index)
            settled += 1
            rock = None

            if (len(chamber) - last_line_before_pattern) % pattern_size_lines == 0:
                display = '|' + f'{chamber[y]:09b}'[1:-1].replace('0', ' ').replace('1', '*') + '|'
                print(display, ', line', len(chamber), ', settled rocks', settled, ', move index', move_index)
    
    
    # with open(outfile_name, 'w') as outfile:
    #     for i, line in enumerate(reversed(chamber)):
    #         n = len(chamber) - 1 - i
    #         display = f'{n:5,} |' + f'{line:09b}'[1:-1].replace('0', ' ').replace('1', '*') + '|'
    #         # print(display)
    #         outfile.write(display + '\n')
    # print('+-------+')
    # print()
    print('tower height', len(chamber) + chamber_offset)

    # 1568513119574 is too high
    # 1568513119573 is too high
    # 1568513119570 is too low
    # Correct answer: 1568513119571


if __name__ == "__main__":
    main()
