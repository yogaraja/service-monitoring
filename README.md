# service-monitoring

# Requirements:
* A service written in python or golang that queries 2 urls (https://httpstat.us/503 & https://httpstat.us/200).
* The service will check the external urls (https://httpstat.us/503 & https://httpstat.us/200 ) are up (based on http status code 200) and response time in milliseconds
* The service will run a simple http service that produces  metrics (on /metrics) and output a prometheus format when hitting the service /metrics url
* Expected response format:

    sample_external_url_up{url="https://httpstat.us/503 "}  = 0
    sample_external_url_response_ms{url="https://httpstat.us/503 "}  = [value]
    sample_external_url_up{url="https://httpstat.us/200 "}  = 1

* [How to build & deploy on desktop](#how-to-build)
    * [Build the Image for the python app](#build-steps)
    * [Run Prometheus & Grafana](#run-prometheus-grafana)    
    * [Run the python app](#run-python-app) 
    * [Urls to access](#url-to-access) 
    * [Generate Test Data](#generate-metrics) 

* [How to deploy on Kubernetes](#how-to-deploy)


## How to build & deploy on desktop

### Build the Image for the python app

```sh
docker build -t service-monitoring .
```

### Run Prometheus & Grafana

```sh
Prometheus: 
Copy the attached prometheus.yml to /tmp. Update the static config depending
on where the python application is deployed.
docker run -d -p 9090:9090 -v /tmp/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus

Grafana:
docker run -d -p 3000:3000 grafana/grafana grafana
```

### Run the python app

```sh
docker run -d -p 5000:5000 service-monitoring
```
### Urls to access

```sh
Python Application: http://localhost:5000/metrics
Prometheus: http://localhost:9090/graph
Grafana: http://localhost:3000/
```

## Generate Test Data
```sh
Run the script attached generateResponseData.sh
./generateResponseData.sh # (This will hit the routes /200 & /503,
so that we can generate some metrics over a time interval
```

## How to deploy on Kubernetes
