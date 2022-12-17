from aocutils import load_input
from copy import copy
import itertools


def main():
    puzzle_input = load_input(__file__)
    # puzzle_input = load_input(__file__, 'example')

    class Valve():
        def __init__(self, name:str, flow:int, tunnels:list[str]) -> None:
            self.name:str = name
            self.flow:int = flow
            self.tunnels:list[str] = tunnels
            self.is_open = False
            self.released = 0
            self.routes:dict[str, list[str]] = {}
        

        def __str__(self) -> str:
            return f'[{self.name} flow {self.flow} -> {",".join(self.tunnels)}]'


        def __repr__(self) -> str:
            return self.__str__()


        def get_route(self, target:str):
            if target in self.routes:
                return self.routes[target]

            routes:list[str] = [[valve] for valve in self.tunnels]
            while True:
                new_routes = []
                for route in routes:
                    route_head:str = route[-1]
                    if route_head == target:
                        self.routes[target] = route
                        return route
                    for valve in valves[route_head].tunnels:
                        if valve not in route:
                            new_routes.append(route + [valve])
                routes = new_routes

        
        def open(self, minute) -> None:
            self.is_open = True
            self.released = self.flow * (30 - (minute + 1))
    

    valves:dict[str, Valve] = {}

    for line in puzzle_input:
        split_line = line.split(' ', maxsplit=9)
        name = split_line[1]
        flow = int(split_line[4].split('=')[1][0:-1])
        tunnels = split_line[9].split(', ')
        valves[name] = Valve(name, flow, tunnels)

    print(valves)

    for valve in valves.values():
        other_valves = set(valves.keys())
        other_valves.remove(valve.name)
        for other in other_valves:
            print(f'from {valve.name} to {other}:')
            print('  ', valve.get_route(other))

    non_zero_valves = [valve.name for valve in valves.values() if valve.flow > 0]
    print(non_zero_valves)
    sequences:list[list[str]] = [list(seq) for seq in itertools.permutations(non_zero_valves)]
    print(f'{len(sequences):,} sequences')

    best_release:int = 0
    for i, sequence in enumerate(sequences):
        if i % 1_000 == 0:
            print('seq', i)
        next_valves = list(sequence)
        # print(next_valves)
        current_valve = valves['AA']
        minute = 0
        release = 0
        while minute < 29 and len(next_valves):
            next_valve = valves[next_valves.pop(0)]
            moves = current_valve.get_route(next_valve.name)
            minute += len(moves) + 1
            release += max(0, 30 - minute) * next_valve.flow
            current_valve = next_valve
        # print(release)
        best_release = max(best_release, release)
    print(best_release)


    # closed_valves:dict[str, Valve] = { name:valve for name,valve in valves.items()}
    # print(closed_valves)
    # open_valves:dict[str, Valve] = {}

    # print('Start')
    # current_valve = valves['AA']
    # released = 0
    # minutes = 30
    # minute = 1
    # while minute <= minutes and len(closed_valves.keys()):
    #     remaining_minutes = minutes - minute
    #     print(minute)

    #     # Find best place to move to
    #     best_next_valve = None
    #     best_next_valve_release = 0
    #     route_to_next = None
    #     for valve in closed_valves.values():
    #         route_to_next = current_valve.get_route(valve.name)
    #         moves = len(route_to_next)
    #         duration = moves + 1
    #         total_release = (remaining_minutes - duration) * valve.flow
    #         if total_release > best_next_valve_release:
    #             best_next_valve = valve
    #             best_next_valve_release = total_release      
        
    #     if current_valve.is_open:
    #         current_valve = valves[route_to_next[0]]
    #         minute += 1
    #         continue

    #     # Open this one or not
    #     open = False
    #     if minute == 28:
    #         open = True
    #     else:
    #         best_next_one_less_min = best_next_valve.flow - best_next_valve.flow
    #         total_release_from_current = current_valve.flow * (remaining_minutes - 1)
    #         total_if_opened = best_next_one_less_min + total_release_from_current

    #     if total_if_opened >= best_next_valve_release:
    #         open = True
        
    #     if open:
    #         del closed_valves[current_valve.name]
    #         open_valves[current_valve.name] = current_valve
    #         current_valve.is_open = True
    #         released += total_release_from_current
    #         minute += 1
    #         print('open', valve.name)
        
    #     current_valve = valves[route_to_next[0]]
    #     print('move to', current_valve.name)
    #     minute += 1

    # print(released)

    # Correct answer: 


if __name__ == "__main__":
    main()
