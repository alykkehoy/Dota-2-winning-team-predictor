from enum import Enum
import pickle
import numpy as np

class ModelType(str, Enum):
    supervised = 'supervised'
    unsupervised = 'unsupervised'
    stacked = 'stacked'

with open('models/supervised.sav', 'rb') as f:
    supervised_model = pickle.load(f)

with open('models/unsupervised.sav', 'rb') as f:
    unsupervised_model = pickle.load(f)

with open('models/naive_bayes.pkl', 'rb') as f:
    naive_bayes = pickle.load(f)

def run_supervised_team(heroes:list):
    heroes = np.array([heroes])
    r_win = supervised_model.predict(heroes)
    return bool(r_win[0])

def run_unsupervised_team(heroes:list):
    heroes = np.array([heroes])
    r_win = unsupervised_model.predict(heroes)
    return bool(r_win[0])

def run_stacked_team(heroes:list):
    heroes = np.array([heroes])
    r_win = bool(unsupervised_model.predict(heroes)[0])
    r_win += bool(supervised_model.predict(heroes)[0])
    r_win += bool(naive_bayes.predict(heroes)[0])

    return r_win > 2
