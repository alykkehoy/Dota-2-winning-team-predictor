import json
import pymongo
import os
import requests
import sys
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

URL = os.getenv("DB_URL")
STEAM_KEY = os.getenv("STEAM_API_KEY")

client = pymongo.MongoClient(URL)
db = client.alpacas_app


""" 
Get current hero list from Valve's API and writes it to the heroes.json file
"""
def get_heroes():
    parameters = {
        "language": "en",
        "key": STEAM_KEY
    }
    response = requests.get("http://api.steampowered.com/IEconDOTA2_570/GetHeroes/v1/", params=parameters)

    if response.status_code == 200:
        json_data = response.json()
        json_data = json_data["result"]["heroes"]
        with open('./json/heroes.json', 'w') as outfile:
            json.dump(json_data, outfile)


""" 
First drops current heroes collection then inserts the heroes from herores.json
"""
def insert_heroes():
    with open('./json/heroes.json') as f:
        heroes = json.load(f)

    db.heroes.drop()
    db.heroes.insert_many(heroes)


""" 
Get current item list from Valve's API and writes it to the items.json file
"""
def get_items():
    parameters = {
        "language": "en",
        "key": STEAM_KEY
    }
    response = requests.get("http://api.steampowered.com/IEconDOTA2_570/GetGameItems/v1", params=parameters)

    if response.status_code == 200:
        json_data = response.json()
        json_data = json_data["result"]["items"]
        with open('./json/items.json', 'w') as outfile:
            json.dump(json_data, outfile)


""" 
First drops current items collection then inserts the items from items.json
"""
def insert_items():
    with open('./json/items.json') as f:
        items = json.load(f)

    db.items.drop()
    db.items.insert_many(items)


""" 
First drops current clusters collection then inserts the clusters from clusters.json
"""
def insert_clusters():
    with open ('./json/clusters.json') as f:
        clusters = json.load(f)
    
    db.clusters.drop()
    db.clusters.insert_many(clusters)


def insert_matches():
    matches = pd.read_csv('./csv/matches_filtered.csv')
    matches_json = matches.to_json(orient='records')
    matches_json = json.loads(matches_json)

    db.matches.drop()
    db.matches.insert_many(matches_json)
    print("Matches Inserted")


def insert_players():
    players = pd.read_csv('./csv/players_filtered.csv')
    players_json = players.to_json(orient='records')
    players_json = json.loads(players_json)

    db.players.drop()
    db.players.insert_many(players_json)
    print("Players Inserted")


def insert_item_stats():
    with open ('./json/item_stats.json') as f:
        item_stats = json.load(f)
    
    db.item_stats.drop()
    db.item_stats.insert_many(item_stats)
    print("Item Stats Inserted")

def insert_hero_stats():
    with open ('./json/hero_stats.json') as f:
        hero_stats = json.load(f)
    
    db.hero_stats.drop()
    db.hero_stats.insert_many(hero_stats)
    print("Hero Stats Inserted")


def main():
    args = sys.argv[1:]
    args = list(arg.lower() for arg in args)

    if 'heroes' in args:
        get_heroes()
        insert_heroes()
    if 'items' in args:
        get_items()
        insert_items()
    if 'clusters' in args:
        insert_clusters()
    if 'matches' in args:
        insert_matches()
    if 'players' in args:
        insert_players()
    if 'item_stats' in args:
        insert_item_stats()
    if 'hero_stats' in args:
        insert_hero_stats()
    

if __name__ == "__main__":
    main()
    