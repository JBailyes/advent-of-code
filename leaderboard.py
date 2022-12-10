import json
import os
import re
import requests

from datetime import datetime, timedelta
from termcolor import colored

containing_dir = os.path.dirname(__file__)

with open(f'{containing_dir}/leaderboard-settings.json', 'r') as settings_file:
    settings = json.load(settings_file)

readable_outfile = f'{containing_dir}/leaderboard.json'
summary_outfile = f'{containing_dir}/leaderboard.txt'

response = requests.get(settings['url'], cookies={ 'session': settings['session'] })
if not response.ok:
    print(response.text)
    exit(1)

raw_data = str(response.text)
data = json.loads(raw_data)

readable_data = json.loads(
        re.sub('_ts": *([0-9]+)',
            lambda match : '_ts":"' + str(datetime.fromtimestamp(int(match.group(1)))) + '"', 
            raw_data))

day_summaries = {}

for member in data['members'].values():
    name = member['name']
    for day_num in sorted(member['completion_day_level']):
        day_info: dict = day_summaries.setdefault(f'{day_num:>02}', {})

        for star_num in sorted(member['completion_day_level'][day_num]):
            star_info: list = day_info.setdefault(star_num, [])
            star = member['completion_day_level'][day_num][star_num]
            star_time_ts = int(star['get_star_ts'])
            star_time = str(datetime.fromtimestamp(star_time_ts))
            star_info.append({ 'name': name, 'time': star_time, 'ts': star_time_ts})
        
        if '2' in member['completion_day_level'][day_num]:
            star_1_ts = day_info['1'][-1]['ts']
            star_2_ts = day_info['2'][-1]['ts']
            diff_total_secs = star_2_ts - star_1_ts
            diff_mins = int(diff_total_secs / 60)
            diff_secs = diff_total_secs - diff_mins * 60
            day_info['2'][-1]['diff'] = f'{diff_mins:>02}:{diff_secs:>02}'
        

for day in sorted(day_summaries):
    day_date = f'2022-12-{day:>02}'
    print(f'Day {day}')
    for star in sorted(day_summaries[day]):
        star_str = '*' * int(star)
        print(colored(f'{star_str:2}  ', 'yellow', attrs=['bold']), end='')
        star_infos = []
        for star_info in sorted(day_summaries[day][star], key=lambda x : x['time']):
            name = star_info['name']
            time = star_info['time'].replace(f'{day_date} ', '')
            diff = f' ({star_info["diff"]})' if 'diff' in star_info else ''
            star_infos.append(f'{time}{diff} {name}')
        print('\n    '.join(star_infos))
        print()


with open(readable_outfile, 'w') as fileout:
    json.dump(readable_data, fileout, indent=4)

