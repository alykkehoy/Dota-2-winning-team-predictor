# Dota 2 Winning Team Predictor (Copy)
This is a public copy of the work our team did in MSCS 710 to create a Dota 2 winning tream predictor.

## Set up
### Anaconda Environment
Load Anaconda environment from `environment.yml`.

```
conda env create -f environment.yml
```

Activate Anaconda environment.
```
conda activate alpaca
```

### Dotenv File
This project uses dotenv to automatically add environment variables needed for authorization to the database and the Steam API. A `.env` file is needed in the root directory with the following contents (filled in with your values).
```
STEAM_API_KEY = "YOUR_KEY_HERE"
DB_URL = "YOUR_URL_HERE"
```

### Running the Server
Within the alpaca environment run `uvicorn main:app` to start the server. This will start the webserver that hosts the API and Dota 2 Draft Assistant site. 

## Mongodb Imports
To import or update data in the mongodb atlas database run `mongodb_import.py` using the arguments below.

### Table of Arguments
Argument | Description
---------|------------
heroes | Current heroes pulled from the Steam API
items | Current items pulled from the Steam API
clusters | Server clusters 
matches | Match data
players | Player data
item_stats | Stats about items from our data
hero_stats | Stats about heroes from our data

### Examples
If you wanted to update the heroes collection in the database you would run: `py mongodb_import.py heroes`

If you wanted to update both items and clusters you would run: `py mongodb_import.py items clusters`

## Match Parser
The match parser continuously gets a sets of matches from the Steam API from a given sequence number or sooner. The current match sequence number is stored in `./csv/sequence_num.txt`. After it retrieves a set of matches it then splits the player info from the match info and saves them in `./csv/players.csv` and `/csv/matches.csv` respectively. Does no data cleaning. Only makes sure the game was played in a ranked lobby.

## Testing - API
Testing is handled using FastAPI's testing client and is run using `pytest`. Every endpoint has at least one test associated with it. 
## Supported Browsers
Chrome
