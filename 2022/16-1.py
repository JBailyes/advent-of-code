from aocutils import load_input
from copy import copy


def main():
    puzzle_input = load_input(__file__)
    puzzle_input = load_input(__file__, 'example')

    class Valve():
        def __init__(self, name:str, flow:int, tunnels:list[str]) -> None:
            self.name:str = name
            self.flow:int = flow
            self.tunnels:list[str] = tunnels
            self.is_open = False
            self.released = 0
        
        def __str__(self) -> str:
            return f'[{self.name} flow {self.flow} -> {",".join(self.tunnels)}]'

        def __repr__(self) -> str:
            return self.__str__()
        
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


    def copy_state(valves:dict[str,Valve]) -> dict[str,Valve]:
        valves_copy:dict[str,Valve] = {}
        for valve in valves.values():
            valves_copy[valve.name] = copy(valve)
        return valves_copy

    
    def evaluate(initial_valves:dict[str,Valve], position:str, open_valve:bool, minute:int, current_plan:list[str]):
        if minute <= 0:
            return ([''], sum([valve.released for valve in initial_valves.values()]))
        valves = copy_state(initial_valves)
        plan:list[str] = copy(current_plan)
        valve = valves[position]

        next_minute = minute - 1
        if open_valve:
            valve.open(minute)
            plan.insert(0, 'open ' + valve.name)
            next_minute -= 1

        best_plan:tuple(list[str], int) = ([''], 0)
        for tunnel in valve.tunnels:
            release_with_open = evaluate(valves, tunnel, True, next_minute, plan)
            if release_with_open[1] > best_plan[1]:
                best_plan = release_with_open

            release_without_open = evaluate(valves, tunnel, False, next_minute, plan)
            if release_without_open[1] > best_plan[1]:
                best_plan = release_without_open
        
        return best_plan
        
    plan, released = evaluate(valves, 'AA', False, 30, (['']))
    print(plan, released)
            

    # Correct answer: 


if __name__ == "__main__":
    main()
