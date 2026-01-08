FROM python:3.9-slim

LABEL maintainer="Gabriel Cristian <gabriel.cristiann@gmail.com>"
LABEL description="A simple custom Prometheus exporter"

WORKDIR /app
COPY . /app
RUN pip3 install -r requirements.txt

CMD ["python3", "exporter.py"]