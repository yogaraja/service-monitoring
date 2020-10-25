FROM python:alpine
RUN mkdir -p /app/service-monitoring && \
    mkdir -p /app/service-monitoring/applications
COPY applications /app/service-monitoring/applications
COPY requirements.txt /app/service-monitoring
RUN cd /app/service-monitoring && pip install -r requirements.txt
EXPOSE 5000 5000
CMD ["python", "/app/service-monitoring/applications/app.py"]