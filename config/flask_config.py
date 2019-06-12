from config import PROJECT_HOME
from os import path

DEBUG = True
LOGGING_CONFIG = "config/logging/local.conf"
APP_NAME = "football-manager"

PORT = 3000
HOST = "127.0.0.1"

USE_S3 = True
USE_RDS = True
DATABASE_NAME = 'msia423'
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = False