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

    ready = int(lines[0])
    print('Departures from', ready)
    smallest_wait = None
    bus_id = None
    for route_time_string in lines[1].split(','):
        if route_time_string == 'x':
            continue
        route_time = int(route_time_string)
        wait = route_time - ready % route_time
        if smallest_wait is None or wait < smallest_wait:
            smallest_wait = wait
            bus_id = route_time

    print('Bus {}, wait {} = {}'.format(bus_id, smallest_wait, bus_id * smallest_wait))


if __name__ == "__main__":
    main()
