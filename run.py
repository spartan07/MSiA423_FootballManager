"""Enables the command line execution of multiple modules within src/

This module combines the argparsing of each module within src/ and enables the execution of the corresponding scripts
so that all module imports can be absolute with respect to the main project directory.

Current commands enabled:

To create a database for Tracks with an initial song:

    `python run.py create --artist="Britney Spears" --title="Radar" --album="Circus"`

To add a song to an already created database:

    `python run.py ingest --artist="Britney Spears" --title="Radar" --album="Circus"`
"""
import argparse
import logging.config
import yaml
import sys
import config

logging.config.fileConfig("config/logging/local.conf")
logger = logging.getLogger("run-football-manager")

from src.load_data import load_s3
from src.create_db import create_db_sql, create_db_rds



if __name__ == '__main__':
    try:
        with open(config.S3_CONFIG, "r") as f:
            s3_config = yaml.load(f)
    except FileNotFoundError:
        logger.error("S3 Config YAML File not Found")
        sys.exit(-1)

    try:
        with open(config.RDS_CONFIG, "r") as f:
            rds_config = yaml.load(f)
    except FileNotFoundError:
        logger.error("DB Config YAML File not Found")
        sys.exit(-1)

    s3_bucket = s3_config["DEST_S3_BUCKET"]
    s3_folder = s3_config["DEST_S3_FOLDER"]
    s3_public =s3_config["PUBLIC_S3"]
    s3_path =s3_config["PATH"]

    db_sql_path = config.SQLALCHEMY_DATABASE_URI
    print(db_sql_path)

    parser = argparse.ArgumentParser(description="Run components")
    subparsers = parser.add_subparsers()

    sub_process = subparsers.add_parser('load',description = "Load data in s3")
    sub_process.add_argument("--public", default=s3_public, help="Public s3 Bucket")
    sub_process.add_argument("--path", default=s3_path, help="Public s3 Path")
    sub_process.add_argument("--s3bucket",default=s3_bucket, help="Destination S3 Bucket location")
    sub_process.add_argument("--s3folder", default=s3_folder, help="Destination S3 Folder Name")
    sub_process.set_defaults(func=load_s3)

    sub_process = subparsers.add_parser('create_sqldb',description = "Create a sqlite db")
    sub_process.add_argument("--engine_string", default=db_sql_path, help="Connection uri for SQLALCHEMY")
    sub_process.set_defaults(func=create_db_sql)

    sub_process = subparsers.add_parser('create_rdsdb',description = "Create a rds db")
    sub_process.add_argument("--user", help="Username for rds")
    sub_process.add_argument("--password", help="Password for rds")
    sub_process.set_defaults(func=create_db_rds)

    args = parser.parse_args()
    args.func(args)