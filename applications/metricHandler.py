#!/usr/bin/python

from flask import request
from prometheus_client import Counter, Histogram, Gauge
import time
import constants

REQUEST_COUNT = Counter('sample_external_url_count', 'Request Count',['app_name', 'method', 'url', 'http_status'])
REQUEST_LATENCY = Gauge('sample_external_url_response_ms', 'Latency in ms', ['url'])
REQUEST_GAUGE = Gauge('sample_external_url_up', 'External url available', ['url'])

def start_timer():
    request.start_time = time.time()

def stop_timer(response):
    resp_time = int ((time.time() - request.start_time) * 1000)  # to get a time in ms
    if request.path == "/200":
        REQUEST_LATENCY.labels(constants.EXTERNAL_URL_200).set(resp_time)
    elif request.path == "/503":
        REQUEST_LATENCY.labels(constants.EXTERNAL_URL_503).set(resp_time)
    else:
        REQUEST_LATENCY.labels("/metrics").set(resp_time)
    return response

def record_request_data(response):
    REQUEST_COUNT.labels('sample_external_url_count', request.method, request.path,
            response.status_code).inc()
    return response

def record_server_up(response):
    if request.path == "/200":
        REQUEST_GAUGE.labels(constants.EXTERNAL_URL_200).set(1.0)
    elif request.path == "/503":
        REQUEST_GAUGE.labels(constants.EXTERNAL_URL_503).set(0.0)
    else:
        REQUEST_GAUGE.labels("/metrics").set(0.0)
    return response

def setup_metrics(app):
    app.before_request(start_timer)
    app.after_request(record_request_data)
    app.after_request(stop_timer)
    app.after_request(record_server_up)
