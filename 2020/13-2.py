import math

from aocutils import load_input


def main():
    puzzle_input = load_input(__file__)
    # puzzle_input = load_input(__file__, 'example')

    # puzzle_input = []
    # puzzle_input.append('')
    # puzzle_input.append('7,13,x,x,59,x,31,19')
    # puzzle_input.append('17,x,13,19')
    # puzzle_input.append('67,7,59,61')
    # puzzle_input.append('67,x,7,59,61')
    # puzzle_input.append('67,7,x,59,61')
    # puzzle_input.append('1789,37,47,1889')

    buses = {}
    route_time_strings = puzzle_input[1].split(',')
    for i in range(len(route_time_strings)):
        route_time_string = route_time_strings[i]
        if route_time_string == 'x':
            continue
        buses[i] = int(route_time_string)
        print(buses[i], 'position', i)

    first_bus = buses[0]
    lcm = first_bus
    if first_bus in buses.keys():
        lcm = math.lcm(first_bus, buses[first_bus])
        print('buses[0] ({}) lcm with buses[{}] ({}) = {}'.format(first_bus, first_bus, buses[first_bus], lcm))

    found = False
    time = lcm - 7
    while not found:
        offsets = list(buses.keys())
        found = True
        for offset in offsets:
            if found and (time + offset) % buses[offset] != 0:
                found = False
        if found:
            print('timestamp:', time)
        else:
            time += lcm


if __name__ == "__main__":
    main()
