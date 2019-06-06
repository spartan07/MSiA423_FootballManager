import logging
import sys
import yaml
import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics

from os import path

rel_path = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(rel_path)

from config import data_loc,model_loc,test_loc

logger  = logging.getLogger(__name__)

def train_model(args):
	config_text = args.config
	model_config = config_text['model']
	try:
		data = pd.read_csv(data_loc + model_config['inp_data'])
		logger.info("Preprocessed data read")
	except FileNotFoundError:
		logger.error("Preprocessed dataframe not found. Run process command")
		sys.exit(-1)

	methods = dict(rforest=RandomForestRegressor,linear_regression=LinearRegression)

	labels = np.array(data[model_config['target']])
	data = data.drop(labels=[model_config['target'], 'Wage', 'Overall'], axis=1)
	features_list = model_config['features_list']

	features = np.array(data[features_list])
	train_features, test_features, train_labels, test_labels = train_test_split(features, labels,test_size=model_config['split_data']['test_size'],
																				random_state=model_config['split_data']['random_state'])

	method = model_config['method']['name']
	assert method in methods.keys()

	rf = RandomForestRegressor(n_estimators=model_config['method']['n_estimators'],
								random_state=model_config['method']['random_state'])
	rf.fit(train_features, train_labels)

	# Save test-dataset
	np.save(test_loc + model_config['outp_test']['feature'], test_features)
	np.save(test_loc + model_config['outp_test']['target'], test_labels)

	with open(model_loc + model_config['save_tmo'], "wb") as f:
		pickle.dump(rf, f)
	logger.info("Trained model object saved to %s", model_loc + model_config['save_tmo'])

