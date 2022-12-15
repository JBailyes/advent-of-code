#!/bin/env python3

import json
import os
import re
import requests

from datetime import datetime
from termcolor import colored

containing_dir = os.path.dirname(__file__)

with open(f'{containing_dir}/leaderboard-settings.json', 'r') as settings_file:
    settings = json.load(settings_file)

readable_outfile = f'{containing_dir}/leaderboard.json'
original_outfile = f'{containing_dir}/leaderboard.original.json'

response = requests.get(settings['url'], cookies={ 'session': settings['session'] })
if not response.ok:
    print(response.text)
    exit(1)

raw_data = str(response.text)
data = json.loads(raw_data)
with open(original_outfile, 'w') as fileout:
    json.dump(data, fileout, indent=4)

readable_data = json.loads(
        re.sub('_ts": *([0-9]+)',
            lambda match : '_ts":"' + str(datetime.fromtimestamp(int(match.group(1)))) + '"', 
            raw_data))
with open(readable_outfile, 'w') as fileout:
    json.dump(readable_data, fileout, indent=4)


class Star():
    def __init__(self, number: int, ts: int, person:str) -> None:
        self.number: int = number
        self.ts: int = ts
        self.person: str = person
    
    def get_ts(self) -> int:
        return self.ts


class Star2(Star):
    def __init__(self, number: int, ts: int, diff:int, person:str) -> None:
        super().__init__(number, ts, person)
        self.diff:int = diff
        self.fastest:bool = False
    
    def get_diff(self) -> int:
        return self.diff


class Day():
    def __init__(self, num:str) -> None:
        self.number = f'{num:>02}'
        self.first_stars: list[Star] = []
        self.second_stars: list[Star] = []
        self.first_star_by_person: dict[str, Star] = {}
        self.second_star_by_person: dict[str, Star] = {}
    
    def add_star(self, star: Star):
        if star.number == 1:
            self.first_stars.append(star)
            self.first_star_by_person[star.person] = star
        else:
            self.second_stars.append(star)
            self.second_star_by_person[star.person] = star
    

days: dict[str, Day] = {}
for day_num in range(1, 25):
    days[day_num] = Day(day_num)

# Get the JSON data into more suitable structures
for member in data['members'].values():
    person = member['name']
    for day_str in sorted(member['completion_day_level']):
        day: Day = days[int(day_str)]
        for star_str in sorted(member['completion_day_level'][day_str]):
            star_num = int(star_str)
            star_time_ts = member['completion_day_level'][day_str][star_str]['get_star_ts']

            if star_num == 1:
                star = Star(star_num, star_time_ts, person)
            else:
                star_1 = day.first_star_by_person[person]
                seconds_between_stars = star_time_ts - star_1.ts
                star = Star2(star_num, star_time_ts, seconds_between_stars, person)

            day.add_star(star)



for day_num in sorted(days):
    day = days[day_num]

    if not day.first_stars:
        continue

    if day.second_stars:
        fastest_2nd = sorted(day.second_stars, key=Star2.get_diff)[0]

    print(f'Day {day_num}')

    day_date = f'2022-12-{day_num:>02} '
    ordered_first_stars:list[Star] = sorted(day.first_stars, key=Star.get_ts)
    ordered_second_stars:list[Star] = sorted(day.second_stars, key=Star.get_ts)

    col_1:list[str] = []
    col_2:list[str] = []

    for star_1 in ordered_first_stars:
        star_time = str(datetime.fromtimestamp(star_1.ts)).replace(day_date, '')
        col_1.append(f'{star_time} {star_1.person}')

    for star_2 in ordered_second_stars:
        star_2_time = str(datetime.fromtimestamp(star_2.ts)).replace(day_date, '')
        seconds_between_stars = star_2.diff
        diff_mins = int(seconds_between_stars / 60)
        diff_secs = seconds_between_stars - diff_mins * 60
        diff_str = f'{diff_mins:>02}:{diff_secs:>02}'
        col_2_text = f'{star_2_time} ({diff_str}) {star_2.person}'
        if star_2 == fastest_2nd:
            col_2.append(colored(col_2_text, 'green', attrs=['bold']))
        else:
            col_2.append(col_2_text)
    
    col_1_width:int = max([len(text) for text in col_1])

    star = colored('*', 'yellow', attrs=['bold'])
    for line in range(len(col_1)):
        col_1_str = f'{star} {col_1[line]:{col_1_width}}'
        col_2_str = f'{star}{star} {col_2[line]}' if len(col_2) > line else ''
        print(f'{col_1_str}    {col_2_str}')
    print()
