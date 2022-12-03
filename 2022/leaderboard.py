import json
import os
import re
import sys

from datetime import datetime

leaderboad_id = sys.argv[1]
leaderboard_download = os.path.dirname(__file__) + f'/leaderboard-{leaderboad_id}.json'
readable_outfile = leaderboard_download.replace('.json', '.readable.json')
summary_outfile = leaderboard_download.replace('.json', '.sumary.txt')

with open(leaderboard_download) as filedata:
    data = filedata.read()

readable_data = json.loads(
        re.sub('_ts": *([0-9]+)',
            lambda match : '_ts":"' + str(datetime.fromtimestamp(int(match.group(1)))) + '"', 
            data))

for member in readable_data['members'].values():
    name = member['name']
    print(name)
    for day_num in sorted(member['completion_day_level']):
        star_times = []
        for star_num in sorted(member['completion_day_level'][day_num]):
            star = member['completion_day_level'][day_num][star_num]
            star_time = star['get_star_ts']
            star_times.append(star_time)
        print(f'   {day_num}: {str(star_times)}')
    print()

with open(readable_outfile, 'w') as fileout:
    json.dump(readable_data, fileout, indent=4)

