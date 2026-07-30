import json
from datetime import datetime
''' 
    This script processes the fixtures data for the 2022/23 Premier League season, 
    and completes all further calculations of stats required for other analysis, such as team matchups for h2h comparisons, team goal stats, and recent form.
'''


'''
    This function extracts unique team ID pairs from the fixtures and saves them to a text file for further analysis or processing. 
    It reads the JSON data from a file, iterates through each fixture, and collects the team IDs in a set to ensure uniqueness. 
    Finally, it saves the unique pairs to a text file.
'''
def extract_unique_team_pairs():
    # 2022/23 SEASON FIXTURES
    with open('fixtures/fixtures_league=39_season=2024.json') as json_file:
        fixtures_file = json.load(json_file) # Load the JSON data from the file into a Python dictionary

    fixture_team_ids = set()  # Set to store unique team ID pairs for all fixtures

    for fixture in fixtures_file.get('response', []):
        home_team_id = fixture.get('teams', {}).get('home', {}).get('id')
        away_team_id = fixture.get('teams', {}).get('away', {}).get('id')

        # Store the team IDs in the set
        fixture_team_ids.add(tuple(sorted([home_team_id, away_team_id])))  # sort to ensure uniqueness regardless of home/away order

    print(f"Total unique team ID pairs for all fixtures: {len(fixture_team_ids)}")
    save_fixtures(fixture_team_ids)  # Save the unique team ID pairs to a text file
    print(f"Unique team ID pairs for all fixtures have been saved to 'remaining_fixtures_for_h2h.txt'.")

def remove_used_fixture(team1_id, team2_id):
    # Read the existing fixtures from the file
    with open("remaining_fixtures_for_h2h.txt", "r") as f:
        fixtures = f.readlines()

    # Create a tuple of the team IDs to remove
    fixture_to_remove = tuple(sorted([team1_id, team2_id]))

    # Filter out the fixture to remove
    updated_fixtures = [fixture for fixture in fixtures if tuple(map(int, fixture.strip()[1:-1].split(','))) != fixture_to_remove]

    print(f"Length before removal: {len(fixtures)}. Removed fixture: {fixture_to_remove}. Remaining fixtures: {len(updated_fixtures)}")

    # Write the updated fixtures back to the file
    save_fixtures([tuple(map(int, fixture.strip()[1:-1].split(','))) for fixture in updated_fixtures])

def save_fixtures(team_ids):
    with open("remaining_fixtures_for_h2h.txt", "w") as f:
        for fixture in team_ids:
            f.write(str(fixture) + "\n")

def extract_fixture_info_for_db(season_start_year):
    with open(f'fixtures/fixtures_league=39_season={season_start_year}.json') as json_file:
        fixtures_file = json.load(json_file) # Load the JSON data from the file into a Python dictionary

    fixture_info = []  # Store all fixture info that will be inserted into database 

    for fixture in fixtures_file.get('response', []):
        f_id = fixture.get('fixture', {}).get('id', {})
        s = fixture.get('league', {}).get('season', {})
        date = datetime.fromisoformat(fixture.get('fixture', {}).get('date', {}))
        ht_id = fixture.get('teams', {}).get('home', {}).get('id')
        at_id = fixture.get('teams', {}).get('away', {}).get('id')
        hgs = fixture.get('goals', {}).get('home', {})
        ags = fixture.get('goals', {}).get('away', {})
        if hgs > ags:
            winner_id = ht_id
        elif ags > hgs:
            winner_id = at_id
        else:
            winner_id = None
        fixture_info.append([f_id, s, date, ht_id, at_id, winner_id, hgs, ags])
    return fixture_info

def extract_h2h_info_for_db(sy, ey, t1_id, t2_id, cf_date):
    try:
        with open(f'20{sy}_{ey}_season_h2h/fixtures_headtohead_h2h={t1_id}-{t2_id}.json') as json_file:
            h2h_file = json.load(json_file) # Load the JSON data from the file into a Python dictionary
    except FileNotFoundError:
        with open(f'20{sy}_{ey}_season_h2h/fixtures_headtohead_h2h={t2_id}-{t1_id}.json') as json_file:
            h2h_file = json.load(json_file) # Load the JSON data from the file into a Python dictionary

    all_info = []  # Store all fixture info that will be inserted into database 

    for h2h in h2h_file.get('response', []):
        # only get fixtures that fit the sets i can use
        if (h2h.get('league', {}).get('season', {}) < 2025) and (h2h.get('league', {}).get('name', {}) == "Premier League"):
            pf_date = datetime.fromisoformat(h2h.get('fixture', {}).get('date', {})).replace(tzinfo=None)
            s = h2h.get('league', {}).get('season', {})
            t1_gs = h2h.get('goals', {}).get('home', {})
            t2_gs = h2h.get('goals', {}).get('away', {})
            if t1_gs > t2_gs:
                winner_id = t1_id
            elif t2_gs > t1_gs:
                winner_id = t2_id
            else:
                winner_id = None
            all_info.append([pf_date, t1_id, t2_id, s, winner_id, t1_gs, t2_gs])

    all_info = sorted(all_info, key=lambda x: x[0]) # sort by date (oldest to newest)
    # list comp and slicing to get most recent 5 past games
    h2h_info = [inf for inf in all_info if inf[0] < cf_date]
    h2h_info = h2h_info[-5:]

    return h2h_info    

def calculate_form_score(fixs, tid):
    if len(fixs) < 5:
        return None
    
    points = 0
    for fix in fixs:
        if fix.winner_team_id == tid:
            points += 3
        elif fix.winner_team_id is None:
            points += 1

    form_score = points / 15
    return form_score

def calculate_h2h_score(h2hs, tid):
    if len(h2hs) < 5:
        return None

    points = 0
    for h2h in h2hs:
        if h2h.winner_team_id == tid:
            points += 3
        elif h2h.winner_team_id is None:
            points += 1

    h2h_score = points / 15
    return h2h_score

#if __name__ == "__main__":
    # extract_unique_team_pairs()
    # extract_seasonal_team_goal_stats()
    # extract_recent_team_form_stats()
    #extract_fixture_info_for_db(2022)
    #extract_h2h_info_for_db(24, 25, 33, 34, datetime.fromisoformat("2024-12-30T20:00:00+00:00"))
