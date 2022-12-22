from aocutils import load_input
from copy import copy


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
            new.release += max(0, 30 - new.minute) * valve.flow

            return new


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
    best_route:Route = None
    evaluated = 0

    # current_valve = valves['AA']
    routes:list[Route] = [Route()]
    while True:
        new_routes:list[Route] = []
        for route in routes:
            for option in non_zero_valves - route.valves_set:
                new_route = route.add(option)
                evaluated += 1
                if new_route.minute < 30:
                    new_routes.append(new_route)
                    if new_route.release > best_release:
                        best_release = new_route.release
                        best_route = new_route
        if not new_routes:
            print('evaluated', evaluated)
            print('best route:', [v.name for v in best_route.valves])
            print('best route release:', best_release)
            exit(1)
        routes = new_routes

    # Correct answer: 1720


if __name__ == "__main__":
    main()
