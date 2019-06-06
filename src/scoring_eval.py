import logging
import sys
import yaml
import pandas as pd
import numpy as np
import pickle
from sklearn.metrics import r2_score

from os import path

rel_path = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(rel_path)

from config import data_loc,model_loc,test_loc

logger  = logging.getLogger(__name__)

def score(args):
	config_text = args.config
	score_config = config_text['score_model']
	try:
		X_test = np.load(test_loc+score_config['inp_name']['feature'])
		y_test = np.load(test_loc+score_config['inp_name']['target'])
	except FileNotFoundError:
		logger.error("Features and target files not found. Run load data command")
		sys.exit(-1)

	with open(model_loc + score_config['path_to_tmo'], "rb") as f:
		rf = pickle.load(f)
		logger.info("Model loaded")

	predictions = rf.predict(X_test)
	pred_act = 10 ** predictions
	test_act = 10 ** y_test

	errors = abs(predictions - y_test)
	print('Mean Absolute Error:', round(np.mean(errors), 2))
	# Print out the MSE
	print('Mean Square Error:', round(np.sum(errors ** 2), 2))

	r2_val = r2_score(test_act, pred_act)

	with open(model_loc+score_config['save_scores'], 'w') as the_file:
		the_file.write('MAE :'+str(round(np.mean(errors), 2))+'\n')
		the_file.write('MSE :'+str(round(np.sum(errors ** 2), 2))+'\n')
		the_file.write('R2 :'+str(round(r2_val, 2))+'\n')
	logger.info("Metrics saved at %s", model_loc+score_config['save_scores'])
