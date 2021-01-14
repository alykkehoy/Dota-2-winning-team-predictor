from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

# test default
def test_default():
    response = client.get("/")
    assert response.status_code == 200

# test heroes
def test_read_heroes():
    response = client.get("/heroes")
    assert response.status_code == 200

def test_read_hero_drow():
    response = client.get("/heroes/6")
    assert response.status_code == 200
    assert response.json() == {
        "name": "npc_dota_hero_drow_ranger",
        "id": 6,
        "localized_name": "Drow Ranger"
        }

def test_read_hero_bad_id():
    response = client.get("/heroes/118")
    assert response.status_code == 404

# test items
def test_read_items():
    response = client.get("/items")
    assert response.status_code == 200

def test_read_item_blink():
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "item_blink",
        "cost": 2250,
        "secret_shop": 0,
        "side_shop": 0,
        "recipe": 0,
        "localized_name": "Blink Dagger"
        }

def test_read_item_bad_id():
    response = client.get("/items/400")
    assert response.status_code == 404

# test clusters
def test_read_clusters():
    response = client.get("/clusters")
    assert response.status_code == 200

def test_read_cluster_us_east():
    response = client.get("/clusters/121")
    assert response.status_code == 200
    assert response.json() == {
        "cluster": 121,
        "region": "US EAST"
        }

def test_read_cluster_bad_id():
    response = client.get("/clusters/1")
    assert response.status_code == 404

# test matches
def test_read_matches():
    response = client.get("/matches")
    assert response.status_code == 200

def test_read_matches_page():
    response = client.get("/matches?sequence_number=4737088502")
    assert response.status_code == 200

def test_read_match_good():
    response = client.get("/matches/5637985930")
    assert response.status_code == 200
    assert response.json() == {
        "radiant_win": True,
        "duration": 3421,
        "pre_game_duration": 90,
        "start_time": 1601530008,
        "match_id": 5637985930,
        "match_seq_num": 4737088312,
        "tower_status_radiant": 1828,
        "tower_status_dire": 0,
        "barracks_status_radiant": 63,
        "barracks_status_dire": 0,
        "cluster": 156,
        "first_blood_time": 179,
        "lobby_type": 7,
        "human_players": 10,
        "leagueid": 0,
        "positive_votes": 0,
        "negative_votes": 0,
        "game_mode": 22,
        "flags": 1,
        "engine": 1,
        "radiant_score": 42,
        "dire_score": 58
        }

def test_read_match_bad():
    response = client.get("/matches/1")
    assert response.status_code == 404

def test_read_match_players_good():
    response = client.get("/matches/5637985930/players")
    assert response.status_code == 200

def test_read_match_players_bad():
    response = client.get("/matches/1/players")
    assert response.status_code == 404

# test stats
def test_read_stats_items():
    response = client.get("/stats/items")
    assert response.status_code == 200

def test_read_stats_items_drow():
    response = client.get("stats/items/6")
    assert response.status_code == 200

def test_read_stats_items_bad():
    response = client.get("stats/items/118")
    assert response.status_code == 404

def test_read_stats_heroes():
    response = client.get("/stats/heroes")
    assert response.status_code == 200

def test_read_stats_hero_drow():
    response = client.get("/stats/heroes/6")
    assert response.status_code == 200

def test_read_stats_hero_bad():
    response = client.get("/stats/heroes/118")
    assert response.status_code == 404

# test models
def test_run_model_supervised():
    response = client.get("model/supervised/1/2/3/4/5/6/7/8/9/10/team")
    assert response.status_code == 200
    assert response.json() == {
        "r_wins": True
        } or {
        "r_wins": False
        }

def test_run_model_supervised():
    response = client.get("model/unsupervised/1/2/3/4/5/6/7/8/9/10/team")
    assert response.status_code == 200
    assert response.json() == {
        "r_wins": True
        } or {
        "r_wins": False
        }

def test_run_model_stacked():
    response = client.get("model/stacked/1/2/3/4/5/6/7/8/9/10/team")
    assert response.status_code == 200
    assert response.json() == {
        "r_wins": True
        } or {
        "r_wins": False
        }
