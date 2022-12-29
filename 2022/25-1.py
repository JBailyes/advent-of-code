from aocutils import load_input


def main():
    puzzle_input = load_input(__file__)
    # puzzle_input = load_input(__file__, 'example')


    def to_dec(snafu:str) -> int:
        digits = {
            '2': 2,
            '1': 1,
            '0': 0,
            '-': -1,
            '=': -2
        }
        decimal = 0
        for i, symbol in enumerate(reversed(snafu)):
            decimal += digits[symbol] * 5**i
        return decimal


    def to_snafu(decimal:int):
        symbols = {
            2: '2',
            1: '1',
            0: '0',
            -1: '-',
            -2: '='
        }
        snafu_bits = to_snafu_arr(decimal)
        return ''.join([symbols[n] for n in snafu_bits])


    def merge(a:list[int], b:list[int]):
        return a[0:len(a) - len(b)] + b

    
    def to_snafu_arr(decimal:int) -> list[int]:
        snafu_bits = []
        snafu = 0
        digit_pos = 0
        if decimal == 0:
            return [0]

        if decimal > 0:
            while snafu < decimal:
                pos_base = 5**digit_pos
                half = (pos_base - 1) / 2

                for mult in [1,2]:
                    snafu = mult * pos_base
                    if snafu == decimal:
                        return [mult] + snafu_bits
                    diff = decimal - snafu
                    if decimal < snafu or decimal <= snafu + half:
                        return [mult] + merge(snafu_bits, to_snafu_arr(diff))
                snafu_bits.append(0)
                digit_pos += 1
        elif decimal < 0:
            while snafu > decimal:
                pos_base = 5**digit_pos
                half = (pos_base - 1) / 2

                for mult in [-1,-2]:
                    snafu = mult * pos_base
                    if snafu == decimal:
                        return [mult] + snafu_bits
                    diff = decimal - snafu
                    if decimal > snafu or decimal >= snafu - half:
                        return [mult] + merge(snafu_bits, to_snafu_arr(diff))
                snafu_bits.append(0)
                digit_pos += 1

    decimal_sum = 0

    for line in puzzle_input:
        decimal = to_dec(line)
        decimal_sum += decimal
        # print(line, '=', decimal, '=', to_snafu(decimal))
    
    print('Decimal sum:', decimal_sum)
    print('SNAFU sum:', to_snafu(decimal_sum))


    # Correct answer: 20-==01-2-=1-2---1-0


if __name__ == "__main__":
    main()
