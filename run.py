"""Enables the command line execution of multiple modules within src/

This module combines the argparsing of each module within src/ and enables the execution of the corresponding scripts
so that all module imports can be absolute with respect to the main project directory.

"""
import argparse
import logging.config
import yaml
import sys
import config
from os import  path

logging.config.fileConfig("config/logging/local.conf")
logger = logging.getLogger("run-football-manager")

from src.load_data import load_s3
from src.create_db import create_db_sql, create_db_rds



if __name__ == '__main__':
	try:
		with open(config.config_path, "r") as f:
			config_text = yaml.load(f)
	except FileNotFoundError:
		logger.error("Config YAML File not Found")
		sys.exit(-1)
	s3_config = config_text['s3']
	if 'rds' in config_text.keys():
		rds_config = config_text['rds']
	if 'sqldb' in config_text.keys():
		sql_config = config_text['sqldb']
		DB_PATH = path.join(config.PROJECT_HOME, sql_config['path'])
		db_sql_path = 'sqlite:///{}'.format(DB_PATH)

	parser = argparse.ArgumentParser(description="Run components")
	subparsers = parser.add_subparsers()

	sub_process = subparsers.add_parser('load',description = "Load data in s3")
	sub_process.add_argument("--config", default=s3_config, help="s3 configurations")
	sub_process.set_defaults(func=load_s3)

	sub_process = subparsers.add_parser('create_sqldb',description = "Create a sqlite db")
	sub_process.add_argument("--engine_string", default=db_sql_path, help="Connection uri for SQLALCHEMY")
	sub_process.set_defaults(func=create_db_sql)

	sub_process = subparsers.add_parser('create_rdsdb',description = "Create a rds db")
	sub_process.add_argument("--user", help="Username for rds")
	sub_process.add_argument("--password", help="Password for rds")
	sub_process.add_argument("--config" , default= rds_config , help ="rds config settings")
	sub_process.set_defaults(func=create_db_rds)

	args = parser.parse_args()
	args.func(args)