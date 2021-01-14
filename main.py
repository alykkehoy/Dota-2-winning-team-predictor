# HOW TO RUN: uvicorn main:app --reload
from model import *

from typing import Optional
from fastapi import FastAPI, HTTPException, Request, Path, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import json
import pymongo
import os

load_dotenv()
URL = os.getenv("DB_URL")

MIN_HERO_ID = 1
MAX_HERO_ID = 129


tags_metadata = [
    {
        "name": "heroes",
        "description": "Information on heroes.",
    },
    {
        "name": "items",
        "description": "Information on items.",
    },
    {
        "name": "clusters",
        "description": "Information on server clusters.",
    },
    {
        "name": "matches",
        "description": "Information on matches and the players in those matches.",
    },
    {
        "name": "models",
        "description": "Ability to run models.",
    },
    {
        "name": "stats",
        "description": "Statistics about our data"
    }
]

app = FastAPI(
    title="Alpacas Dota 2 App",
    description="API for Alpacas Dota 2 draft assistant and website.",
    version='1.0',
    openapi_tags=tags_metadata
)

# mount static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/")
def root(request: Request):
    json_data = get_heroes()
    return templates.TemplateResponse("index.html", {"request": request, "response": json_data})

@app.get("/heroes", tags=['heroes'], description='Get all heroes.')
def get_heroes():
    client = pymongo.MongoClient(URL)
    db = client.alpacas_app
    
    json_data = list(db.heroes.find({}, {"_id": 0}).sort([("id", 1)]))

    client.close()
    return json_data

@app.get("/heroes/{hero_id}", tags=['heroes'], description='Get hero information for a given hero id.')
def get_hero(hero_id: int = Path(..., description='The ID of the hero to get.', ge=MIN_HERO_ID, le=MAX_HERO_ID)):
    client = pymongo.MongoClient(URL)
    db = client.alpacas_app

    json_data = db.heroes.find_one({"id": hero_id}, {"_id": 0})

    if json_data is None:
        client.close()
        raise HTTPException(status_code=404, detail="Hero not found")

    client.close()
    return json_data

@app.get("/items", tags=['items'], description='Get all items.')
def get_items():
    client = pymongo.MongoClient(URL)
    db = client.alpacas_app

    json_data = list(db.items.find({}, {"_id": 0}))

    client.close()
    return json_data

@app.get("/items/{item_id}", tags=['items'], description='Get item details for a given item id.')
def get_item(item_id:int):
    client = pymongo.MongoClient(URL)
    db = client.alpacas_app

    json_data = db.items.find_one({"id": item_id}, {"_id": 0})

    if json_data is None:
        client.close()
        raise HTTPException(status_code=404, detail="Item not found")

    client.close()
    return json_data

@app.get("/clusters", tags=['clusters'], description='Get all cluster information.')
def get_clusters():
    client = pymongo.MongoClient(URL)
    db = client.alpacas_app

    json_data = list(db.clusters.find({}, {"_id": 0}))

    client.close()
    return json_data

@app.get("/clusters/{cluster_id}", tags=['clusters'], description='Get a specific cluster\'s information for a given cluster id.')
def get_cluster(cluster_id: int):
    client = pymongo.MongoClient(URL)
    db = client.alpacas_app
    
    json_data = db.clusters.find_one({"cluster": cluster_id}, {"_id": 0})

    if json_data is None:
        client.close()
        raise HTTPException(status_code=404, detail="Cluster not found")

    client.close()
    return json_data

@app.get("/matches", tags=['matches'], description='Get matches starting at a provided match sequence number. If no match sequence number is provided start at the earliest match.')
def get_matches(sequence_number: int = Query(None, description='Match sequence number to start at.', ge=1)):
    client = pymongo.MongoClient(URL)
    db = client.alpacas_app

    json_data = {}
    if sequence_number is not None:
        json_data = list(db.matches.find({"match_seq_num": {"$gt": sequence_number}}, {"_id": 0}, limit=50))
    else:
        json_data = list(db.matches.find({}, {"_id": 0}, limit=50))
    
    client.close()
    return json_data

@app.get("/matches/{match_id}", tags=['matches'], description='Get detailed match information for a given match id.')
def get_match(match_id: int):
    client = pymongo.MongoClient(URL)
    db = client.alpacas_app
    
    json_data = db.matches.find_one({"match_id": match_id}, {"_id": 0})

    if json_data is None:
        client.close()
        raise HTTPException(status_code=404, detail="Match not found")

    client.close()
    return json_data


@app.get("/matches/{match_id}/players", tags=['matches'], description='Get players for a given match id.')
def get_match_players(match_id: int):
    client = pymongo.MongoClient(URL)
    db = client.alpacas_app

    json_data = list(db.players.find({"match_id": match_id}, {"_id": 0}))

    if not json_data:
        client.close()
        raise HTTPException(status_code=404, detail="Players not found")

    client.close()
    return json_data

@app.get("/stats/items", tags=['stats'], description='Get all stats about items.')
def get_items_stats():
    client = pymongo.MongoClient(URL)
    db = client.alpacas_app

    json_data = list(db.item_stats.find({}, {"_id": 0}))

    client.close()
    return json_data

@app.get("/stats/items/{hero_id}", tags=['stats'], description='Get all stats about items for a specific hero.')
def get_item_stats(hero_id: int = Path(..., description='The ID of the hero to get item stats for.', ge=MIN_HERO_ID, le=MAX_HERO_ID)):
    client = pymongo.MongoClient(URL)
    db = client.alpacas_app

    json_data = list(db.item_stats.find({"hero_id": hero_id}, {"_id": 0}))

    if not json_data:
        client.close()
        raise HTTPException(status_code=404, detail="Item stats for given hero id not found")
    
    client.close()
    return json_data

@app.get("/stats/heroes", tags=['stats'], description='Get all stats about heroes.')
def get_heroes_stats():
    client = pymongo.MongoClient(URL)
    db = client.alpacas_app

    json_data = list(db.hero_stats.find({}, {"_id": 0}))

    client.close()
    return json_data

@app.get("/stats/heroes/{hero_id}", tags=['stats'], description='Get all stats about a specific hero.')
def get_hero_stats(hero_id: int = Path(..., description='The ID of the hero to get stats for.', ge=MIN_HERO_ID, le=MAX_HERO_ID)):
    client = pymongo.MongoClient(URL)
    db = client.alpacas_app

    json_data = list(db.hero_stats.find({"hero_id": hero_id}, {"_id": 0}))

    if not json_data:
        client.close()
        raise HTTPException(status_code=404, detail="Hero stats for given hero id not found")

    client.close()
    return json_data  

@app.get("/model/{model_type}/{r_1}/{r_2}/{r_3}/{r_4}/{r_5}/{d_1}/{d_2}/{d_3}/{d_4}/{d_5}/team",
        tags=['models'],
        description='Run a given model to predict winning team.')
def run_model(model_type:ModelType = Path(..., description='Type of model to run.'),
                r_1: int = Path(None, description='The ID of Radiant hero 1.', ge=MIN_HERO_ID, le=MAX_HERO_ID),
                r_2: int = Path(None, description='The ID of Radiant hero 2.', ge=MIN_HERO_ID, le=MAX_HERO_ID),
                r_3: int = Path(None, description='The ID of Radiant hero 3.', ge=MIN_HERO_ID, le=MAX_HERO_ID),
                r_4: int = Path(None, description='The ID of Radiant hero 4.', ge=MIN_HERO_ID, le=MAX_HERO_ID),
                r_5: int = Path(None, description='The ID of Radiant hero 5.', ge=MIN_HERO_ID, le=MAX_HERO_ID),
                d_1: int = Path(None, description='The ID of Dire hero 1.', ge=MIN_HERO_ID, le=MAX_HERO_ID),
                d_2: int = Path(None, description='The ID of Dire hero 2.', ge=MIN_HERO_ID, le=MAX_HERO_ID),
                d_3: int = Path(None, description='The ID of Dire hero 3.', ge=MIN_HERO_ID, le=MAX_HERO_ID),
                d_4: int = Path(None, description='The ID of Dire hero 4.', ge=MIN_HERO_ID, le=MAX_HERO_ID),
                d_5: int = Path(None, description='The ID of Dire hero 5.', ge=MIN_HERO_ID, le=MAX_HERO_ID)):

    heroes = [r_1, r_2, r_3, r_4, r_5, d_1, d_2, d_3, d_4, d_5]
    r_wins = None

    if model_type == ModelType.supervised:
        r_wins = run_supervised_team(heroes)
    elif model_type == ModelType.unsupervised:
        r_wins = run_unsupervised_team(heroes)
    elif model_type == ModelType.stacked:
        r_wins = run_stacked_team(heroes)

    return {'r_wins': r_wins}