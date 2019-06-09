import boto3
import logging
import botocore
from os import path
import sys

logger = logging.getLogger(__name__)

rel_path = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(rel_path)

from config import data_loc


def load_data(args):
	"""
	Copies raw dataset from public S3 bucket to user-defined bucket and folder
	:param args: s3 configurations from config.yaml file
	:return: None
	"""
	if args.type == "s3":
		config = args.config
		s3_config = config['load']['s3']
		object_name = s3_config['DEST_S3_FOLDER']+"EA_FIFA_19.csv"
		s3 = boto3.resource('s3')
		copy_source = {
			'Bucket': s3_config['PUBLIC_S3'],
			'Key': s3_config['PATH']
		}
		bucket = s3.Bucket(s3_config['DEST_S3_BUCKET'])
		try:
			bucket.copy(copy_source, object_name)
			logger.info("Raw data copied succesfully!")
		except botocore.exceptions.NoCredentialsError as e:
			logger.error(e)
	else:
		config = args.config
		local_config = config['load']['local']
		s3_config = config['load']['s3']
		s3 = boto3.resource('s3')
		source_bucket = s3.Bucket(s3_config['PUBLIC_S3'])
		try:
			source_bucket.download_file(s3_config['PATH'], data_loc+'EA_FIFA_19.csv')
		except botocore.exceptions.NoCredentialsError as e:
			logger.error(e)
			sys.exit(1)



