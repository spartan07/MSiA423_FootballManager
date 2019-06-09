import logging
import sys
import os
import io
import boto3
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
	if args.type =="s3":
		s3_config = config_text['load']['s3']
		try:
			s3 = boto3.resource('s3')
			obj = s3.Object(s3_config['DEST_S3_BUCKET'], s3_config['DEST_S3_FOLDER']+score_config['inp_name']['feature'])
			with io.BytesIO(obj.get()["Body"].read()) as f:
				# rewind the file
				f.seek(0)
				X_test = np.loadtxt(f)
			obj = s3.Object(s3_config['DEST_S3_BUCKET'], s3_config['DEST_S3_FOLDER']+score_config['inp_name']['target'])
			with io.BytesIO(obj.get()["Body"].read()) as f:
				# rewind the file
				f.seek(0)
				y_test = np.loadtxt(f)
		except FileNotFoundError:
			logger.error("Test files. Run model command")
			sys.exit(-1)
		#Load model
		s3 = boto3.resource('s3')
		with io.BytesIO() as data:
			s3.Bucket(s3_config['DEST_S3_BUCKET']).download_fileobj(s3_config['DEST_S3_FOLDER']+score_config['path_to_tmo'], data)
			data.seek(0)  # move back to the beginning after writing
			rf = pickle.load(data)
			logger.info("Model loaded")

	else:
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

	with open(model_loc + score_config['save_scores'], 'w') as the_file:
		the_file.write('MAE :' + str(round(np.mean(errors), 2)) + '\n')
		the_file.write('MSE :' + str(round(np.sum(errors ** 2), 2)) + '\n')
		the_file.write('R2 :' + str(round(r2_val, 2)) + '\n')

	if args.type =="s3":
		s3 = boto3.resource('s3')
		BUCKET = "test"
		s3.Bucket(s3_config['DEST_S3_BUCKET']).upload_file(model_loc + score_config['save_scores'],
		                                                   s3_config['DEST_S3_FOLDER']+ score_config['save_scores'])
		os.remove(model_loc + score_config['save_scores'])
	else:
		logger.info("Metrics saved at %s", model_loc + score_config['save_scores'])

