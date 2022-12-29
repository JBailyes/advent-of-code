from aocutils import load_input
from copy import copy
from itertools import permutations, combinations


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
    

    class Route():
        def __init__(self) -> None:
            self.valves:list[Valve] = [valves['AA']]
            self.minute:int = 0
            self.release:int = 0
            self.valves_set:set[Valve] = set(self.valves)
            self.str = str(self.valves)

        def add(self, valve:Valve):
            new = Route()
            new.valves = copy(self.valves)
            new.valves_set = copy(self.valves_set)
            new.minute = self.minute
            new.release = self.release

            moves = new.valves[-1].get_route(valve.name)
            new.minute += len(moves) + 1
            new.valves.append(valve)
            new.valves_set.add(valve)
            new.release += max(0, 26 - new.minute) * valve.flow
            new.str = str(new.valves)
            return new
        
        def __str__(self) -> str:
            return self.str

        def __hash__(self) -> int:
            return self.str.__hash__()


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
            valve.get_route(other)
            # print(f'from {valve.name} to {other}:')
            # print('  ', valve.get_route(other))

    non_zero_valves:set[Valve] = set([valve for valve in valves.values() if valve.flow > 0])
    print('non-zero valves', non_zero_valves)

    best_release:int = 0
    best_routes:tuple[Route,Route] = None
    evaluated = 0
    route_generations = 0

    route_pairs:list[tuple[Route,Route]] = [(Route(), Route())]
    while True:
        new_route_pairs:list[tuple[Route,Route]] = []
        for route_m, route_e in route_pairs:
            if len(route_m.valves) == 1:
                options = combinations(non_zero_valves - route_m.valves_set - route_e.valves_set, r=2)
            else:
                options = permutations(non_zero_valves - route_m.valves_set - route_e.valves_set, r=2)
            for opt_m, opt_e in options:
                new_route_m = route_m.add(opt_m)
                new_route_e = route_e.add(opt_e)
                evaluated += 1
                if evaluated % 1_000_000 == 0:
                    print(f'evaluated {evaluated:,d}')
                if new_route_m.minute < 26 and new_route_e.minute < 26:
                    new_route_pair = (new_route_m, new_route_e)
                    pair_release = new_route_m.release + new_route_e.release
                    if pair_release > best_release:
                        best_release = pair_release
                        best_routes = new_route_pair
                    if new_route_m.minute < 24 and new_route_e.minute < 24:
                        new_route_pairs.append(new_route_pair)
        route_generations += 1
        print('route generations:', route_generations, f'evaluated {evaluated:,d}')
        if not new_route_pairs:
            print('evaluated', evaluated)
            print('best routes:')
            print(' me', [v.name for v in best_routes[0].valves])
            print(' elephant', [v.name for v in best_routes[1].valves])
            print('best route release:', best_release)
            exit(1)
        route_pairs = new_route_pairs

    # Wrong answer 2549 - too low

    # Correct answer: 


if __name__ == "__main__":
    main()
