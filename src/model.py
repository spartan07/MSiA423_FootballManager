import logging
import sys
import boto3
import botocore
import pandas as pd
import numpy as np
import pickle
from io import StringIO
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
	if args.type =="s3":
		try:
			s3_config = config_text['load']['s3']
			client = boto3.client('s3')
			obj = client.get_object(Bucket=s3_config['DEST_S3_BUCKET'],
									Key=s3_config['DEST_S3_FOLDER']+model_config['inp_data'])
			data = pd.read_csv(obj['Body'])
		except botocore.exceptions.NoCredentialsError as e:
			logger.error(e)
	else:
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
	if args.type =="s3":
		pickle_byte_obj = pickle.dumps(rf)
		s3_resource = boto3.resource('s3')
		s3_resource.Object(s3_config['DEST_S3_BUCKET'], s3_config['DEST_S3_FOLDER']+model_config['save_tmo']).put(Body=pickle_byte_obj)


		csv_buffer = StringIO()
		np.save(csv_buffer, test_features)
		s3_resource = boto3.resource('s3')
		s3_resource.Object(s3_config['DEST_S3_BUCKET'], s3_config['DEST_S3_FOLDER']+model_config['outp_test']['feature']).put(Body=csv_buffer.getvalue())

		csv_buffer = StringIO()
		np.save(csv_buffer, test_labels)
		s3_resource = boto3.resource('s3')
		s3_resource.Object(s3_config['DEST_S3_BUCKET'], s3_config['DEST_S3_FOLDER']+model_config['outp_test']['target']).put(Body=csv_buffer.getvalue())

	else:
		np.save(test_loc + model_config['outp_test']['feature'], test_features)
		np.save(test_loc + model_config['outp_test']['target'], test_labels)
		with open(model_loc + model_config['save_tmo'], "wb") as f:
			pickle.dump(rf, f)
		logger.info("Trained model object saved to %s", model_loc + model_config['save_tmo'])

