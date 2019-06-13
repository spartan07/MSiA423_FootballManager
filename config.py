from os import path
PROJECT_HOME = path.dirname(path.abspath(__file__))

config_path = path.join(PROJECT_HOME, 'config/config.yml')
data_loc= path.join(PROJECT_HOME, 'data/')
model_loc = path.join(PROJECT_HOME, 'models/')
test_loc = path.join(PROJECT_HOME, 'test/')
LOGGING_CONFIG = "config/logging/local.conf"




