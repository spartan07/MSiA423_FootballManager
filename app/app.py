import flask
import pickle
from os import path
import sys
import yaml
import logging
# Use pickle to load in the pre-trained model.
rel_path = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(rel_path)

import config

logger = logging.getLogger(__name__)
from src.predict_case import predict,knn_manip

try:
    with open(config.config_path, "r") as f:
        config_text = yaml.load(f)
except FileNotFoundError:
    logger.error("Config YAML File not Found")
    sys.exit(-1)
app = flask.Flask(__name__, template_folder='templates')
app.secret_key = "super secret key"

app_config = config_text['app']


@app.route('/', methods=['GET', 'POST'])
def main():
    if flask.request.method == 'GET':
        return flask.render_template('main.html')
    if flask.request.method == 'POST':
        inp = {}
        for elem in app_config['input_list']:
            flask.flash(elem)
            inp[elem] = flask.request.form[elem]
        prediction = predict(inp)
        nname = knn_manip(inp)
        print(nname)
        return flask.render_template('main.html',
                                     original_input= inp,
                                     result=prediction,
                                     knn_out=nname
                                     )


if __name__ == '__main__':
    app.run(debug=True)