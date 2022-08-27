#!/usr/bin/env python

"""
Fetch and cache FPL bootstrap data.
"""

import datetime
import json
import lzma
from pathlib import Path
import requests

def main():
    
    url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    cache = Path('cache')
    
    # Fetch the FPL bootstrap JSON.
    print(f'Fetching {url}... ', end='', flush=True)
    r = requests.get(url)
    if not r.ok:
        print(f'Failed: {r.status_code}.')
        exit(1)
    print('OK.')

    # Prettify the JSON so it can be diffed.
    print(f'Prettifying JSON... ', end='', flush=True)
    pretty = json.dumps(r.json(), indent=4, sort_keys=True)
    print(f'OK.')

    # Prepare the cache file path.
    now = datetime.datetime.today()
    path = cache / Path(f'{now.year}/{now.month}/{now.day}/{now.hour:02d}{now.minute:02d}.json.xz')
    path.parent.mkdir(parents=True, exist_ok=True)

    # Compress the JSON into the cache.
    print(f'Compressing into {path}... ', end='', flush=True)
    with lzma.open(path, 'wt', encoding='utf-8') as f:
        f.write(pretty)
    print(f'OK.')

if __name__ == '__main__':
    main()
