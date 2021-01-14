import json
import os
import requests
import datetime
import time
import csv
from enum import Enum
from dotenv import load_dotenv

load_dotenv()
STEAM_KEY = os.getenv("STEAM_API_KEY")


""" 
Enum for skill level. Defined by Valve
"""
class Skill(Enum):
    ANY = 0
    NORMAL = 1
    HIGH = 2
    VERY_HIGH = 3


"""
Ranked lobby type value. Defined by valve
"""
RANKED_LOBBY_TYPE = 7

num_new_matches = 0


"""
Get a set of matches from the Steam API from the sequence number or sooner. Splits the player
info from the match and saves them in the players.csv and matches.csv respectively. Does no cleaning
only makes sure the game is played in a ranked lobby. Returns the most recent match sequence number
or None if no matches were found.

@param match_seq_num The match sequence number to start at
"""
def get_match_history_sequence(match_seq_num):
    global num_new_matches
    num_new_matches = 0
    new_matches = []
    new_players = []

    parameters = {
        "start_at_match_seq_num": match_seq_num,
        "key": STEAM_KEY
    }

    response = requests.get("http://api.steampowered.com/IDOTA2Match_570/GetMatchHistoryBySequenceNum/v1", params=parameters)

    if response.status_code == 200:
        json_data = response.json()
        matches = json_data['result']['matches']

        for match in matches:
            if match['lobby_type'] == RANKED_LOBBY_TYPE:
                match.pop('picks_bans')
                match.pop('dire_captain', None)
                match.pop('radiant_captain', None)

                players = match.pop('players')

                for player in players:
                    player.update({'match_id': match['match_id']})
                    player.pop('ability_upgrades', None) 
                    player.pop('additional_units', None)

                    
                new_players += players
                new_matches.append(match)
                
        num_new_matches = len(new_matches)
        write_csv('./csv/players.csv', new_players)
        write_csv('./csv/matches.csv', new_matches)

        new_seq_num = matches[-1]['match_seq_num']
        with open ('./csv/sequence_num.txt', 'w') as f:
            f.write(str(new_seq_num))
        return new_seq_num
        
    return None


"""
Appends data to a csv. If the file does not exist it creates it and inserts the header row.

@param file_name File path to the csv
@param data Data to be appended to the csv
"""
def write_csv(file_name, data: list):
    if len(data) > 0:
        if os.path.exists(file_name):
            with open (file_name, 'a') as outfile:
                writer = csv.DictWriter(outfile, fieldnames=data[0].keys())
                writer.writerows(data)
        else:
            with open (file_name, 'a') as outfile:
                writer = csv.DictWriter(outfile, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)


"""
Continuously calls get_match_history_sequence every 10 seconds till interrupted. 
"""
def get_match_history_sequence_continuous():

    match_seq_num = None

    with open ('./csv/sequence_num.txt', 'r') as f:
        match_seq_num = f.read()

    try:
        total_matches = 0
        while True:
            new_match_seq_num = get_match_history_sequence(match_seq_num)
            if new_match_seq_num is not None:
                match_seq_num = new_match_seq_num

                total_matches += num_new_matches
                print(datetime.datetime.now().strftime("[%m-%d-%Y %H:%M:%S]"))
                print("Matches added: " + str(num_new_matches))
                print("Total matches added: " + str(total_matches), end="\n\n")
            
            time.sleep(10)

    except KeyboardInterrupt:
        pass


def main():
    get_match_history_sequence_continuous()


if __name__ == "__main__":
    main()
