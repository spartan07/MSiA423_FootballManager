from os import path
PROJECT_HOME = path.dirname(path.abspath(__file__))
config_path = path.join(PROJECT_HOME, 'config/config.yml')

DEBUG = True
LOGGING_CONFIG = "config/logging/local.conf"
PORT = 9038
APP_NAME = "Football_Manager"
#DB_PATH = path.join(PROJECT_HOME,'data/msia423.db')
#SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(DB_PATH)
#DATABASE_NAME = 'msia423'
#SQLALCHEMY_TRACK_MODIFICATIONS = True
HOST = "127.0.0.1"



