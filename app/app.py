import flask
from os import path
from flask_sqlalchemy import SQLAlchemy
from src.create_db import user_input
import sys
import yaml
import logging
import math
import os
import boto3
import io
import pickle
import pandas as pd

# Use pickle to load in the pre-trained model.
rel_path = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(rel_path)
import config

logger = logging.getLogger(__name__)
from src.predict_case import predict, knn_manip

try:
	with open(config.config_path, "r") as f:
		config_text = yaml.load(f)
except FileNotFoundError:
	logger.error("Config YAML File not Found")
	sys.exit(-1)

app = flask.Flask(__name__, template_folder='templates')
app.secret_key = "super secret key"
app.config.from_pyfile('../config/flask_config.py')


app_config = config_text['app']
s3_config = config_text['s3']
score_config = config_text['score_model']
model_config = config_text['model']
predict_config = config_text['predict']

if app.config['USE_RDS']:
	aws_config = config_text['rds']
	conn_type = aws_config['type']
	host = aws_config['host']
	port = aws_config['port']
	database = aws_config['dbname']
	user = os.environ.get('MYSQL_USER')
	password = os.environ.get('MYSQL_PASSWORD')
	app.config['SQLALCHEMY_DATABASE_URI'] = '{}://{}:{}@{}:{}/{}'. \
		format(conn_type, user, password, host, port, database)

if app.config['USE_S3']:
	try:
		s3 = boto3.resource('s3')
		with io.BytesIO() as data:
			s3.Bucket(s3_config['DEST_S3_BUCKET']).download_fileobj(
				s3_config['DEST_S3_FOLDER'] + score_config['path_to_tmo'], data)
			data.seek(0)  # move back to the beginning after writing
			rf = pickle.load(data)
			logger.info("Model loaded")

		client = boto3.client('s3')
		obj = client.get_object(Bucket=s3_config['DEST_S3_BUCKET'], Key=s3_config['DEST_S3_FOLDER'] + config_text['pre_process']['processed'])
		processed = pd.read_csv(obj['Body'])
		obj = client.get_object(Bucket=s3_config['DEST_S3_BUCKET'], Key=s3_config['DEST_S3_FOLDER'] + config_text['pre_process']['adhoc'])
		adhoc = pd.read_csv(obj['Body'])
	except FileNotFoundError as e:
		logger.error(e)

else:
	try:
		with open(config.model_loc + predict_config['path_to_tmo'], "rb") as f:
			rf = pickle.load(f)
		logger.info("Model loaded")
	except FileNotFoundError as e:
		logger.error(e)
	try:
		processed = pd.read_csv(config.data_loc+config_text['pre_process']['processed'])
		adhoc = pd.read_csv(config.data_loc+config_text['pre_process']['adhoc'])
	except FileNotFoundError as e:
		logger.error(e)

millnames = ['', 'K', ' M', ' B', ' T']
def millify(n):
	n = float(n)
	millidx = max(0, min(len(millnames) - 1,
						 int(math.floor(0 if n == 0 else math.log10(abs(n)) / 3))))

	return '{:.0f}{}'.format(n / 10 ** (3 * millidx), millnames[millidx])

db = SQLAlchemy(app)

@app.route('/', methods=['GET', 'POST'])
def main():
	return flask.render_template('main2.html')


@app.route('/results', methods=['GET', 'POST'])
def run():
	inp = {}
	for elem in app_config['input_list']:
		inp[elem] = flask.request.form[elem]
	prediction = float(predict(rf, inp))

	nname, nid, npos = knn_manip(inp, processed, adhoc)
	print(nname)

	try:
		userinp = user_input(Reactions=inp['Reactions'], \
		                     Potential=inp['Potential'], \
		                     Age=inp['Age'], \
		                     BallControl=inp['BallControl'], \
		                     StandingTackle=inp['StandingTackle'], \
		                     Composure=inp['Composure'], \
		                     Dribbling=inp['Dribbling'], \
		                     Positioning=inp['Positioning'], \
		                     Finishing=inp['Finishing'], \
		                     GKReflexes=inp['GKReflexes'],
		                     Position=inp['Position'], \
		                     Predicted_Val=prediction)

		db.session.add(userinp)
		db.session.commit()
		logger.info('New user input     added')
	except Exception as e:
		logger.error(e)
		sys.exit(-1)

	return flask.render_template('results.html', original_input=inp, result="GBP " + millify(int(prediction)), knn_out=nname, knn_pic=nid, knn_pos=npos)


def start_app(args):
	"""Start application and choose to store user input in sqlite or rdsss
		Args:
			args: arguments including app specific configurations and specifications
		Returns:
			NA
	"""
	app.run(debug=app.config['DEBUG'], port=app.config['PORT'], host=app.config['HOST'])