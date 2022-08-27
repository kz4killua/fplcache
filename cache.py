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
        player = pd.DataFrame(player['history'])
        player.to_csv(DATA_DIR / f'{id}.csv', index=False)

    # Keep track of when last we saved player data.
    with open(last_checked_path, 'w') as f:
        json.dump(last_checked_event, f) 
        
    return

if __name__ == '__main__':
    main()
