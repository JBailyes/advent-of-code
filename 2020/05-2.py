import argparse


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()

    lines = []
    with open(args.input, 'r') as infile:
        for line in infile:
            lines.append(line.strip())

    seat_ids = []

    for seat_referecne in lines:
        row_reference = seat_referecne[0:7]
        col_reference = seat_referecne[7:10]

        row_binary = row_reference.replace('F', '0').replace('B', '1')
        col_binary = col_reference.replace('L', '0').replace('R', '1')

        row_number = int(row_binary, 2)
        col_number = int(col_binary, 2)

        seat_id = row_number * 8 + col_number
        seat_ids.append(seat_id)

    seat_ids = sorted(seat_ids)

    print('{} seats, {} to {}'.format(len(seat_ids), seat_ids[0], seat_ids[-1]))

    last_seat = seat_ids[0]
    print(last_seat)
    for seat in seat_ids[1:]:
        print(seat)
        if seat > last_seat + 1:
            print('My seat:', last_seat + 1)  # 699 is the answer for my input
            exit()
        last_seat = seat


if __name__ == "__main__":
    main()
