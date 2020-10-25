#!/usr/bin/python
###############################################################################
# This is a Flask RESTful api server app.
# The service will check for external urls are up based on http status 200 and
# response time
# The service will run a http service that produces metrics (on /metrics)
#
###############################################################################
import os
import logging
import prometheus_client
import requests
import constants
from flask import Flask, jsonify, Response
from flask_cors import CORS
from metricHandler import setup_metrics
from logging.handlers import RotatingFileHandler
from requests.exceptions import HTTPError

app = Flask(__name__)
CORS(app)
setup_metrics(app)

CONTENT_TYPE_LATEST = str('text/plain; version=0.0.4; charset=utf-8')
APP_DIR = '/opt/deployment/applications'
LOG_DIR = '/var/log/service-monitoring/'

# Setup logging:
# application_server.log - This is the main log for this server process.
def config_logger():
    if not os.path.isdir(LOG_DIR):
        os.mkdir(LOG_DIR)

    app.logger.setLevel(logging.INFO)
    # create file handler which logs even debug messages
    fh = RotatingFileHandler(LOG_DIR + '/application_server.log', 1000000, 5)
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    # create formatter and add it to the handlers
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    formatter = logging.Formatter('%(asctime)s -%(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    app.logger.addHandler(fh)
    app.logger.addHandler(ch)

@app.route('/')
def get_service_root():
    app.logger.info("From service route: /")
    return jsonify(message='Response OK')

@app.route('/200', methods=['GET'])
def reply_from_service_200():
    app.logger.info("From service route: 200")
    return getExternalUrl(constants.EXTERNAL_URL_200)

@app.route('/503', methods=['GET'])
def reply_from_service_503():
    app.logger.info("From service route: 503")
    return getExternalUrl(constants.EXTERNAL_URL_503)

@app.route('/metrics', methods=['GET'])
def metrics():
    return Response(prometheus_client.generate_latest(), mimetype=CONTENT_TYPE_LATEST)

def getExternalUrl(url):
    try:
        response = requests.get(url)
        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
        return jsonify(response.text)
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        print('Success!', response.url)
        return jsonify(response.text)

# program main entry point
if __name__ == '__main__':
    config_logger()
    app.run(host='0.0.0.0', port=5000, debug=False)
