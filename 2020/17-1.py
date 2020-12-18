from aocutils import load_input


def main():
    puzzle_input = load_input(__file__)
    # puzzle_input = load_input(__file__, 'example')

    initial_state = {}
    x_bounds = {min: 0, max: 0}
    y_bounds = {min: 0, max: 0}
    z_bounds = {min: 0, max: 0}

    def update_bounds(pos):
        x_bounds[min] = min(x_bounds[min], pos.x)
        x_bounds[max] = max(x_bounds[max], pos.x)
        y_bounds[min] = min(y_bounds[min], pos.y)
        y_bounds[max] = max(y_bounds[max], pos.y)
        z_bounds[min] = min(z_bounds[min], pos.z)
        z_bounds[max] = max(z_bounds[max], pos.z)

    def store_state(pos, state_store, value):
        update_bounds(pos)
        state_store[pos] = value

    def get_state(pos, state_store):
        if pos not in state_store:
            return False
        return state_store[pos]

    for y, line in enumerate(puzzle_input):
        z = 0
        for x, state in enumerate(line):
            pos = Pos(x, y, z)
            if state == '#':
                store_state(pos, initial_state, True)

    print(initial_state)

    def get_neighbours(pos):
        positions = set()
        for x in pos.x - 1, pos.x, pos.x + 1:
            for y in pos.y - 1, pos.y, pos.y + 1:
                for z in pos.z - 1, pos.z, pos.z + 1:
                    positions.add(Pos(x, y, z))
        positions.remove(pos)
        return positions

    def count_active_neighbours(pos, state_store):
        active = 0
        for neighbouring_pos in get_neighbours(pos):
            if get_state(neighbouring_pos, state_store):
                active += 1
        return active

    def all_positions():
        positions = []
        for x in range(x_bounds[min] - 1, x_bounds[max] + 2):
            for y in range(y_bounds[min] - 1, y_bounds[max] + 2):
                for z in range(z_bounds[min] - 1, z_bounds[max] + 2):
                    positions.append(Pos(x, y, z))
        return positions

    current_states = initial_state
    for cycle in range(6):
        new_states = {}
        for pos in all_positions():
            active = get_state(pos, current_states)
            active_neighbours = count_active_neighbours(pos, current_states)
            if active and active_neighbours in [2, 3] \
                    or (not active and active_neighbours == 3):
                store_state(pos, new_states, True)
        current_states = new_states

    print('total active:', len(current_states))


class Pos:
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z
        self._hash = z * 1000 + y * 100 + x

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __repr__(self):
        return '({},{},{})'.format(self.x, self.y, self.z)

    def __hash__(self):
        return self._hash


if __name__ == "__main__":
    main()
