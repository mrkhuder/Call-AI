FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

COPY pipelines /app/pipelines
COPY config.yml /app/config.yml

CMD ["python", "-m", "pipelines.no_show", "--config", "config.yml"]
