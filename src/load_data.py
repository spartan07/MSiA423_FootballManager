import boto3
import logging
import botocore

logger = logging.getLogger(__name__)


def load_s3(args):
	"""
	Copies raw dataset from public S3 bucket to user-defined bucket and folder
	:param args: s3 configurations from config.yaml file
	:return: None
	"""
	s3_config = args.config
	object_name = s3_config['DEST_S3_FOLDER']+"/EA_FIFA_19.csv"
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



