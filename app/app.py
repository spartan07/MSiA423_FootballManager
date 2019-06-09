import flask
import pickle
from os import path
import sys
import yaml
import logging
import math

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

millnames = ['', 'K', ' M', ' B', ' T']


def millify(n):
    n = float(n)
    millidx = max(0, min(len(millnames) - 1,
                         int(math.floor(0 if n == 0 else math.log10(abs(n)) / 3))))

    return '{:.0f}{}'.format(n / 10 ** (3 * millidx), millnames[millidx])


@app.route('/', methods=['GET', 'POST'])
def main():
    return flask.render_template('main2.html')


@app.route('/results', methods=['GET', 'POST'])
def run():
    inp = {}
    for elem in app_config['input_list']:
        flask.flash(elem)
        inp[elem] = flask.request.form[elem]
    prediction = predict(inp)

    nname, nid = knn_manip(inp)
    print(nname)
    return flask.render_template('results.html',
                                 original_input=inp,
                                 result="GBP " + millify(int(prediction)),
                                 knn_out=nname,
                                 knn_pic=nid
                                 )
def start_app(args):
    """Start application and choose to store user input in sqlite or rds
        Args:
            args: arguments including app specific configurations and specifications
        Returns:
            NA
    """
    app.run(debug=app.config['DEBUG'], port=app.config['PORT'], host=app.config['HOST'])