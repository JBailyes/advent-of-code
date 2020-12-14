import argparse
import os


def main():
    day = os.path.basename(__file__).split('-')[0]
    challenge_input = '{}-input.txt'.format(day)
    # challenge_input = '{}-example.txt'.format(day)

    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default=challenge_input)
    args = parser.parse_args()

    lines = []
    with open(args.input, 'r') as infile:
        for line in infile:
            lines.append(line.strip())

    lines = []
    lines.append('')
    lines.append('7,13,x,x,59,x,31,19')
    # lines.append('17,x,13,19')
    # lines.append('67,7,59,61')
    # lines.append('67,x,7,59,61')
    # lines.append('67,7,x,59,61')
    # lines.append('1789,37,47,1889')

    buses = {}
    route_time_strings = lines[1].split(',')
    for i in range(len(route_time_strings)):
        route_time_string = route_time_strings[i]
        if route_time_string == 'x':
            continue
        buses[i] = int(route_time_string)

    found = False
    time = 0
    while not found:
        offsets = list(buses.keys())
        found = True
        for offset in offsets:
            if found and (time + offset) % buses[offset] != 0:
                found = False
        if found:
            print('timestamp:', time)
        else:
            time += buses[0] * buses[offsets[1]]


if __name__ == "__main__":
    main()
