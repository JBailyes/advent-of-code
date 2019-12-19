from os.path import basename
import colorama


class Pattern:
    def __init__(self, length: int, digit_repeat: int):
        self.len = length
        self.full_pattern = []
        base_pattern = [0, 1, 0, -1]

        repeated_digits = []
        for i in range(0, len(base_pattern)):
            for j in range(0, digit_repeat):
                repeated_digits.append(base_pattern[i])

        for i in range(0, length + 1):
            digit = repeated_digits[i % len(repeated_digits)]
            self.full_pattern.append(digit)

        self.full_pattern.pop(0)

    def get(self, pos):
        return self.full_pattern[pos]


class FFT:
    def __init__(self, input_list: list):
        self.input = input_list
        self.input_len = len(input_list)

    def phase(self, phase_input: list) -> list:
        output = []
        for output_pos in range(0, self.input_len):
            pattern = Pattern(self.input_len, output_pos + 1)
            total = 0
            for pos, input_number in enumerate(phase_input):
                # print('{0}*{1} '.format(input_number, pattern.get(pos)), end='')
                total += input_number * pattern.get(pos)
            result = total % 10
            # print('=', result)
            output.append(result)
        # print(output)
        # print('')
        return output

    def run(self, phase_count: int) -> list:
        phase_input = self.input
        phase_output = phase_input
        for i in range(0, phase_count):
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

    # lines = [
    #     # '12345678'
    #     # '80871224585914546619083218645595'
    #     # '19617804207202209144916044189917'
    #     '69317163492948606335995924319873'
    # ]

    input_list = []
    for digit in lines[0]:
        input_list.append(int(digit))

    pattern = Pattern(8, 8)
    print(pattern.full_pattern)

    result = FFT(input_list).run(100)
    print('result', result[0:8])


if __name__ == "__main__":
    main()
