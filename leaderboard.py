import json
import os
import re
import requests

from datetime import datetime

containing_dir = os.path.dirname(__file__)

with open(f'{containing_dir}/leaderboard-settings.json', 'r') as settings_file:
    settings = json.load(settings_file)

readable_outfile = f'{containing_dir}/leaderboard.json'
summary_outfile = f'{containing_dir}/leaderboard.txt'

response = requests.get(settings['url'], cookies={ 'session': settings['session'] })
if not response.ok:
    print(response.text)
    exit(1)

data = str(response.text)

readable_data = json.loads(
        re.sub('_ts": *([0-9]+)',
            lambda match : '_ts":"' + str(datetime.fromtimestamp(int(match.group(1)))) + '"', 
            data))

day_summaries = {}

for member in readable_data['members'].values():
    name = member['name']
    for day_num in sorted(member['completion_day_level']):
        star_times = []
        for star_num in sorted(member['completion_day_level'][day_num]):

            day_info: dict = day_summaries.setdefault(day_num, {})
            star_info: list = day_info.setdefault(star_num, [])

            star = member['completion_day_level'][day_num][star_num]
            star_time = star['get_star_ts']
            star_info.append({ 'name': name, 'time': star_time})

for day in sorted(day_summaries):
    day_date = f'2022-12-{day:>02}'
    print(f'Day {day}')
    for star in sorted(day_summaries[day]):
        star_str = '*' * int(star)
        print(f'{star_str:2}  ', end='')
        star_infos = []
        for star_info in sorted(day_summaries[day][star], key=lambda x : x['time']):
            name = star_info['name']
            time = star_info['time'].replace(f'{day_date} ', '')
            star_infos.append(f'{time} {name}')
        print('\n    '.join(star_infos))
        print()


with open(readable_outfile, 'w') as fileout:
    json.dump(readable_data, fileout, indent=4)

