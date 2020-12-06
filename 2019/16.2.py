from os.path import basename
import colorama


class FFT:
    def __init__(self, input_list: list):
        self.starting_input_list = input_list
        self.input_size = len(self.starting_input_list) * 10_000
        self.message_offset = int(''.join([str(i) for i in input_list[0:7]]))
        self.base_pattern = [0, 1, 0, -1]

    def pattern_at(self, pos: int, repeat_factor: int):
        pattern_len = 4 * repeat_factor
        normalised_pos = (pos + 1) % pattern_len
        return self.base_pattern[int(normalised_pos / repeat_factor)]

    def phase(self, phase_input: list) -> list:
        output = []
        for repeat_factor in range(1, self.input_size + 1):
            total = 0
            first_non_zero = repeat_factor - 1
            for pos in range(first_non_zero, self.input_size):
                # pos = i + self.message_offset
                total += phase_input[pos] * self.pattern_at(pos, repeat_factor)
            result = total % 10
            output.append(result)

            # pattern_len = 4 * repeat_factor
            #
            # # After this many pos the combo of multiplied input and pattern will start to repeeat
            # pattern_and_input_repeat_len = pattern_len * len(self.input_len
            #
            # # My input len is 650, examples are much shorteer, so pattern_and_input_repeat_len
            # # will always be less than input len * 10,0000
            #
            # subtotal = 0
            # for pos in range(0, pattern_and_input_repeat_len):
            #     subtotal += phase_input[pos % len(phase_input)] * self.pattern_at(pos, repeat_factor)
            #
            # num_repeats = int(self.input_len / pattern_and_input_repeat_len)
            # total = 0
            # total += subtotal * num_repeats
            #
            # # Get the leftover bits after the final repeat
            # current_pos = num_repeats * pattern_and_input_repeat_len
            # end_pos = current_pos + self.input_len % pattern_and_input_repeat_len
            # for pos in range(current_pos, end_pos):
            #     total += phase_input[pos % len(phase_input)] * self.pattern_at(pos, repeat_factor)
            #
            # result = total % 10
            # output.append(result)
        return output

    def calculate(self, phase_count: int) -> list:
        phase_input = []
        for pos in range(0, len(self.starting_input_list) * 10_000):
            phase_input.append(self.starting_input_list[pos % len(self.starting_input_list)])

        phase_output = None
        for i in range(0, phase_count):
            # print('phase', i + 1)
            phase_output = self.phase(phase_input)
            phase_input = phase_output
        return phase_output


def main():
    colorama.init()

    inputFile = basename(__file__)[:2] + '-input.txt'
    lines = []
    with open(inputFile,  'r') as infile:
        for line in infile:
            lines.append(line.strip())

    lines = [
        '03036732577212944063491565474664'
    ]

    input_list = []
    for digit in lines[0]:
        input_list.append(int(digit))

    fft = FFT(input_list)
    print('message offset:', fft.message_offset)
    final_output = fft.calculate(100)
    print(final_output)
    print('result', ''.join(str(i) for i in final_output))


if __name__ == "__main__":
    main()
