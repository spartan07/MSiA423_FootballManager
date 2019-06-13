import sys
from os import path
import yaml
import logging
import pickle

rel_path = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(rel_path)
logger = logging.getLogger(__name__)

from src.preprocess_data import value_to_int, check_contract, major_nation, simple_position, right_footed
from src.predict_case import predict, knn_manip
from config import model_loc
from config import config_path, data_loc

try:
    with open(config_path, "r") as f:
        config_text = yaml.load(f)
except FileNotFoundError as e:
    logger.error("FIle not founf")

score_config = config_text['score_model']
import pandas as pd
sample = pd.DataFrame({'ID': {0: 158023},
                       'Name': {0: 'L. Messi'},
                       'Age': {0: 31},
                       'Photo': {0: 'https://cdn.sofifa.org/players/4/19/158023.png'},
                       'Nationality': {0: 'Argentina'},
                       'Flag': {0: 'https://cdn.sofifa.org/flags/52.png'},
                       'Overall': {0: 94},
                       'Potential': {0: 94},
                       'Club': {0: 'FC Barcelona'},
                       'Club Logo': {0: 'https://cdn.sofifa.org/teams/2/light/241.png'},
                       'Value': {0: '€110.5M'},
                       'Wage': {0: '€565K'},
                       'Special': {0: 2202},
                       'Preferred Foot': {0: 'Left'},
                       'International Reputation': {0: 5.0},
                       'Weak Foot': {0: 4.0},
                       'Skill Moves': {0: 4.0},
                       'Work Rate': {0: 'Medium/ Medium'},
                       'Body Type': {0: 'Messi'},
                       'Real Face': {0: 'Yes'},
                       'Position': {0: 'RF'},
                       'Jersey Number': {0: 10.0},
                       'Joined': {0: 'Jul 1, 2004'},
                       'Loaned From': {0: None},
                       'Contract Valid Until': {0: '2021'},
                       'Height': {0: "5'7"},
                       'Weight': {0: '159lbs'},
                       'LS': {0: '88+2'},
                       'ST': {0: '88+2'},
                       'RS': {0: '88+2'},
                       'LW': {0: '92+2'},
                       'LF': {0: '93+2'},
                       'CF': {0: '93+2'},
                       'RF': {0: '93+2'},
                       'RW': {0: '92+2'},
                       'LAM': {0: '93+2'},
                       'CAM': {0: '93+2'},
                       'RAM': {0: '93+2'},
                       'LM': {0: '91+2'},
                       'LCM': {0: '84+2'},
                       'CM': {0: '84+2'},
                       'RCM': {0: '84+2'},
                       'RM': {0: '91+2'},
                       'LWB': {0: '64+2'},
                       'LDM': {0: '61+2'},
                       'CDM': {0: '61+2'},
                       'RDM': {0: '61+2'},
                       'RWB': {0: '64+2'},
                       'LB': {0: '59+2'},
                       'LCB': {0: '47+2'},
                       'CB': {0: '47+2'},
                       'RCB': {0: '47+2'},
                       'RB': {0: '59+2'},
                       'Crossing': {0: 84.0},
                       'Finishing': {0: 95.0},
                       'HeadingAccuracy': {0: 70.0},
                       'ShortPassing': {0: 90.0},
                       'Volleys': {0: 86.0},
                       'Dribbling': {0: 97.0},
                       'Curve': {0: 93.0},
                       'FKAccuracy': {0: 94.0},
                       'LongPassing': {0: 87.0},
                       'BallControl': {0: 96.0},
                       'Acceleration': {0: 91.0},
                       'SprintSpeed': {0: 86.0},
                       'Agility': {0: 91.0},
                       'Reactions': {0: 95.0},
                       'Balance': {0: 95.0},
                       'ShotPower': {0: 85.0},
                       'Jumping': {0: 68.0},
                       'Stamina': {0: 72.0},
                       'Strength': {0: 59.0},
                       'LongShots': {0: 94.0},
                       'Aggression': {0: 48.0},
                       'Interceptions': {0: 22.0},
                       'Positioning': {0: 94.0},
                       'Vision': {0: 94.0},
                       'Penalties': {0: 75.0},
                       'Composure': {0: 96.0},
                       'Marking': {0: 33.0},
                       'StandingTackle': {0: 28.0},
                       'SlidingTackle': {0: 26.0},
                       'GKDiving': {0: 6.0},
                       'GKHandling': {0: 11.0},
                       'GKKicking': {0: 15.0},
                       'GKPositioning': {0: 14.0},
                       'GKReflexes': {0: 8.0},
                       'Release Clause': {0: '€226.5M'}})

inp = {'Reactions':96,'Potential':94,'Age':33,'BallControl':94,'StandingTackle':31,'Composure':95,
 'Dribbling':88, 'Positioning':95,'Finishing':94,'GKReflexes':11,'Simple_Position_AM':0,'Simple_Position_DF':0,
       'Simple_Position_DM':0,'Simple_Position_GK':0,'Simple_Position_MF':0,'Simple_Position_ST':1}

inp2 = {'Reactions':96,'Potential':94,'Age':33,'BallControl':94,'StandingTackle':31,'Composure':95,
 'Dribbling':88, 'Positioning':95,'Finishing':94,'GKReflexes':11,'Position':'ST'}


def test_value():
    sample['Wage'] = sample['Wage'].apply(value_to_int)
    assert sample['Wage'][0] == 565000.0


def test_contract():
    sample2 = sample.apply(check_contract, axis=1)
    assert sample2['contract_days'][0] == 1097


def test_nation():
    sample2 = major_nation(sample)
    assert sample2['Nationality'][0] == 0


def test_position():
    sample['Simple_Position'] = sample.apply(simple_position, axis=1)
    assert sample['Simple_Position'][0] == 'ST'


def test_right():
    sample['Right_Foot'] = sample.apply(right_footed, axis=1)
    assert sample['Right_Foot'][0] == 0


def test_predict():
    try:
        with open(model_loc + score_config['path_to_tmo'], "rb") as f:
            rf = pickle.load(f)
        logger.info("Model loaded")
    except FileNotFoundError as e:
        logger.error(e)
    val = predict(rf, inp)
    assert round(val/1000000,-1) == 90


def test_knn():
    try:
        processed = pd.read_csv(data_loc + config_text['pre_process']['processed'])
        adhoc = pd.read_csv(data_loc + config_text['pre_process']['adhoc'])
    except FileNotFoundError as e:
        logger.error(e)
    nname, nid, npos = knn_manip(inp2, processed, adhoc)
    assert len(nname) == len(nid) == len(npos) == config_text['app']['neighbors']