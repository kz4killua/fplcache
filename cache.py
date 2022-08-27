#!/usr/bin/env python

"""
Fetch and cache FPL bootstrap data.
"""

import datetime
import json
import lzma
from pathlib import Path
import requests

import pandas as pd
import api
import data

def main():
    
    # Gather and unpack data
    print('Gathering data...')
    general_data = api.get_general_data()
    fixtures = pd.DataFrame(api.get_fixtures())
    season = data.get_current_season(fixtures)
    elements = pd.DataFrame(general_data['elements'])
    events = pd.DataFrame(general_data['events'])
    
    # Prepare the data directory
    DATA_DIR = Path(f'data/api/{season}/players')
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    last_checked_event = data.get_last_checked_event(events)
    last_checked_path = DATA_DIR / 'last_checked.json'
    
    # Quit if the data is already up to date
    if last_checked_path.exists():
        with open(last_checked_path, 'r') as f:
            if json.load(f) == last_checked_event:
                return

    # Update player data.   
    for id in elements['id'].unique():
        player = api.get_player_data(id)
        player = pd.DataFrame(data['history'])
        player.to_csv(DATA_DIR / f'{id}.csv', index=False)

    # Keep track of when last we saved player data.
    with open(last_checked_path, 'w') as f:
        json.dump(last_checked_event, f) 
        
    return
    
    
    
    url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    cache = Path('data')
    
    season = '2022-23'
    DATA_DIR = Path(f'data/api/{season}/players')
    DATA_DIR.mkdir(parents=True, exist_ok=True)
   
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
    # path = cache / Path(f'{now.year}/{now.month}/{now.day}/{now.hour:02d}{now.minute:02d}.json.xz')
    path = DATA_DIR / Path(f'{now.hour:02d}{now.minute:02d}.json.xz')
    # path.parent.mkdir(parents=True, exist_ok=True)

    # Compress the JSON into the cache.
    print(f'Compressing into {path}... ', end='', flush=True)
    with lzma.open(path, 'wt', encoding='utf-8') as f:
        f.write(pretty)
    print(f'OK.')

if __name__ == '__main__':
    main()
