import boto3
import logging
import botocore
import argparse
import yaml
import sys
from os import path

rel_path = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(rel_path)

import config
logger = logging.getLogger(__name__)


def load_s3(args):
    """
    Copies raw dataset from public S3 bucket to user-defined bucket and folder
    :param args: User arguments for public s3 path, public s3 folder, destination s3 bucket, destination s3 folder
    :return: None
    """
    object_name = args.s3folder+"/EA_FIFA_19.csv"
    s3 = boto3.resource('s3')
    copy_source = {
        'Bucket': args.public,
        'Key': args.path
    }
    bucket = s3.Bucket(args.s3bucket)
    try:
        bucket.copy(copy_source, object_name)
    except botocore.exceptions.NoCredentialsError as e:
        logger.error(e)

if __name__ == '__main__':
    try:
        with open(config.S3_CONFIG, "r") as f:
            s3_config = yaml.load(f)
    except FileNotFoundError:
        logger.error("YAML File not Found")
        sys.exit(-1)

    s3_bucket = s3_config["DEST_S3_BUCKET"]
    s3_folder = s3_config["DEST_S3_FOLDER"]
    s3_public =s3_config["PUBLIC_S3"]
    s3_path =s3_config["PATH"]

    parser = argparse.ArgumentParser(description="Run components")
    subparsers = parser.add_subparsers()

    sub_process = subparsers.add_parser('load',description = "Load data in s3")

    sub_process.add_argument("--public", default=s3_public, help="Public s3 Bucket")
    sub_process.add_argument("--path", default=s3_path, help="Public s3 Path")
    sub_process.add_argument("--s3bucket",default=s3_bucket, help="Destination S3 Bucket location")
    sub_process.add_argument("--s3folder", default=s3_folder, help="Destination S3 Folder Name")
    sub_process.set_defaults(func=load_s3)

    args = parser.parse_args()
    args.func(args)

