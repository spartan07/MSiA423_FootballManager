import logging
import sys
import yaml
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsRegressor

from os import path
rel_path = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(rel_path)
import config

logger = logging.getLogger(__name__)

try:
	with open(config.config_path, "r") as f:
		config_text = yaml.load(f)
except FileNotFoundError:
	logger.error("Config YAML File not Found")
	sys.exit(-1)

# inp = {'Reactions':65,'Potential':80,'Age':25,'BallControl':79,'StandingTackle':80,'Composure':80,
# 'Dribbling':65,'Positioning':90,'Finishing':80,'GKReflexes':90,'Position':'CAM'}

def simple_position(df):
    if df['Position'] == 'GK':
        return 'GK'
    elif (df['Position'] == 'RB') | (df['Position'] == 'LB') | (df['Position'] == 'CB') | (df['Position'] == 'LCB') | (df['Position'] == 'RCB') | (df['Position'] == 'RWB') | (df['Position'] == 'LWB'):
        return 'DF'
    elif (df['Position'] == 'LDM') | (df['Position'] == 'CDM') | (df['Position'] == 'RDM'):
        return 'DM'
    elif (df['Position'] == 'LM') | (df['Position'] == 'LCM') | (df['Position'] == 'CM') | (df['Position'] == 'RCM') | (df['Position'] == 'RM'):
        return 'MF'
    elif (df['Position'] == 'LAM') | (df['Position'] == 'CAM') | (df['Position'] == 'RAM') | (df['Position'] == 'LW') | (df['Position'] == 'RW'):
        return 'AM'
    elif (df['Position'] == 'RS') | (df['Position'] == 'ST') | (df['Position'] == 'LS') | (df['Position'] == 'CF') | (df['Position'] == 'LF') | (df['Position'] == 'RF'):
        return 'ST'
    else:
        return df.Position


def knn_manip(inp):
	predict_config = config_text['predict']
	df = pd.DataFrame(inp, index=[0])
	df['Simple_Position'] = df.apply(simple_position, axis=1)
	my_cols_list = predict_config['pos_list']
	df = df.reindex(columns=[*df.columns.tolist(), *my_cols_list], fill_value=0)
	req_simp = df['Simple_Position'].values[0]
	col_name = 'Simple_Position_' + req_simp
	df[col_name] = 1
	df.drop(labels=['Position', 'Simple_Position'], axis=1, inplace=True)

	# Find neighbors from processed data
	processed = pd.read_csv(config.data_loc+'processed_fifa.csv')
	adhoc = pd.read_csv(config.data_loc+'adhoc.csv')
	features_list = predict_config['features_list'] + [col for col in processed.columns if col.startswith('Simple_')]
	position_data = processed.loc[processed[col_name] == 1, :]
	y_train = position_data['Value']
	X_train = position_data[features_list]

	scaler = StandardScaler()
	scaler.fit(X_train)
	X_train = scaler.transform(X_train)
	df = scaler.transform(df)

	regressor = KNeighborsRegressor(n_neighbors=5)
	regressor.fit(X_train, y_train)
	nneighbors = position_data.iloc[regressor.kneighbors(df)[1][0], :]
	nneighbor_id = nneighbors['ID'].tolist()
	nname = adhoc.loc[adhoc['ID'].isin(nneighbor_id),'Name'].tolist()

	#adhoc = adhoc.loc[adhoc['ID'].isin(nneighbor_id),:]
	#adhoc.to_csv(config.data_loc+'neighbor.csv', index=False)
	return nname


def predict(inp):
	predict_config = config_text['predict']
	with open(config.model_loc + predict_config['path_to_tmo'], "rb") as f:
		rf = pickle.load(f)
		logger.info("Model loaded")
	df = pd.DataFrame(inp, index=[0])
	features_list = predict_config['features_list']
	features = np.array(df[features_list])
	market_val = 10**(rf.predict(features)[0])
	return market_val





