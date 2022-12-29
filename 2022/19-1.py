import re
from aocutils import load_input
from copy import copy


def main():
    class Blueprint():
        def __init__(self, ore_robot_ore, clay_robot_ore, obs_robot_ore, obs_robot_clay,
         geo_robot_ore, geo_robot_obs) -> None:
            self.ore_robot_ore = ore_robot_ore
            self.clay_robot_ore = clay_robot_ore
            self.obs_robot_ore = obs_robot_ore
            self.obs_robot_clay = obs_robot_clay
            self.geo_robot_ore = geo_robot_ore
            self.geo_robot_obs = geo_robot_obs

        def __str__(self) -> str:
            return f'Orebot = {self.ore_robot_ore} ore, Claybot = {self.clay_robot_ore} ore, ' \
                   f'Obsbot = {self.obs_robot_ore} ore and {self.obs_robot_clay} clay, ' \
                   f'Geobot = {self.geo_robot_ore} ore and {self.geo_robot_obs} obs'
    

    class Resources():
        def __init__(self) -> None:
            self.ore:int = 0
            self.clay:int = 0
            self.obs:int = 0
            self.geo:int = 0
    
    
    class Robots():
        def __init__(self) -> None:
            self.ore:int = 1
            self.clay:int = 0
            self.obs:int = 0
            self.geo:int = 0

    
    class Scenario():
        def __init__(self, minutes:int, bp:Blueprint, res:Resources, robots:Robots) -> None:
            pass


    puzzle_input = load_input(__file__)
    puzzle_input = load_input(__file__, 'example')

    blueprints:list[Blueprint] = []
    for line in puzzle_input:
        [_, ore_robot_ore, clay_robot_ore, obs_robot_ore, obs_robot_clay,
         geo_robot_ore, geo_robot_obs] = [int(d) for d in re.findall('\d+', line)]
        blueprints.append(Blueprint(ore_robot_ore, clay_robot_ore, obs_robot_ore, obs_robot_clay,
                  geo_robot_ore, geo_robot_obs))
    

    def build_options(bp:Blueprint, res:Resources) -> list[int]:
        ore_robot_options = int(res.ore / bp.ore_robot_ore)
        clay_robot_options = int(res.ore / bp.clay_robot_ore)
        obs_robot_options = min(int(res.ore / bp.obs_robot_ore), int(res.clay / bp.obs_robot_clay))
        geo_robot_options = min(int(res.ore / bp.geo_robot_ore), int(res.obs / bp.geo_robot_obs))
        return [ore_robot_options, clay_robot_options, obs_robot_options, geo_robot_options]


    res:Resources = Resources()
    robots:Robots = Robots()
    bp:Blueprint = blueprints[0]
    print(bp)
    for minute in range(24):
        print('minute', minute + 1)
        build_ore = 0
        build_clay = 0
        build_obs = 0
        build_geo = 0
        [ore_robot_options, clay_robot_options, obs_robot_options, geo_robot_options] = build_options(bp, res)
        if geo_robot_options:
            res.ore -= bp.geo_robot_ore
            res.obs -= bp.geo_robot_obs
            print('build geo')
            build_geo = 1
        elif obs_robot_options:
            res.ore -= bp.obs_robot_ore
            res.clay -= bp.obs_robot_clay
            print('build obs')
            build_obs = 1
        elif clay_robot_options and res.clay < bp.obs_robot_clay - robots.clay * 2:
            res.ore -= bp.clay_robot_ore
            print('build clay')
            build_clay = 1
        elif ore_robot_options:
            res.ore -= ore_robot_options * bp.ore_robot_ore
            print('build ore')
            build_ore = 1
        
        res.ore += robots.ore
        res.clay += robots.clay
        res.obs += robots.obs
        res.geo += robots.geo

        robots.ore += build_ore
        robots.clay += build_clay
        robots.obs += build_obs
        robots.geo += build_geo
    
    print(res.geo)

    # Correct answer: 


if __name__ == "__main__":
    main()
