import argparse


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()

    lines = []
    with open(args.input, 'r') as infile:
        for line in infile:
            lines.append(line.strip())

    highest_seat = 0

    for seat_referecne in lines:
        row_reference = seat_referecne[0:7]
        col_reference = seat_referecne[7:10]

        row_binary = row_reference.replace('F', '0').replace('B', '1')
        col_binary = col_reference.replace('L', '0').replace('R', '1')

        row_number = int(row_binary, 2)
        col_number = int(col_binary, 2)

        seat_id = row_number * 8 + col_number

        highest_seat = max(highest_seat, seat_id)

        print('{} {} = {} {} = row {}, col {}, seat {}'.format(
            row_reference, col_reference, row_binary, col_binary, row_number, col_number, seat_id))

    print('Highest seat reference:', highest_seat)


if __name__ == "__main__":
    main()
