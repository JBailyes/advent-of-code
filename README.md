# Advent of Code

https://adventofcode.com/

I started 2015's challenge in 2020, using Python 3.9

2018 was probably done in one of Python 3.4, 3.5 or 3.6

2019 was probably Python 3.7

2020 started in Python 3.7, but quickly switched to 3.9

2022 Python 3.11


`leaderboard.py` loads `leaderboard-settings.json`, which is expected to contain a URL and session cookie value, e.g:

```json
{
    "url": "https://adventofcode.com/2022/leaderboard/private/view/xxx.json",
    "session": "xyz"
}
```

You can find your session ID by inspecting (via your browser's dev tools) request headers that your browser sends when visiting/refreshing the URL
