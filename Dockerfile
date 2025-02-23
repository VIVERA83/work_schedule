FROM python:3.12.3-slim-bullseye

WORKDIR app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UVICORN_WORKERS=1

ENV PORT=8008
ENV HOST=0.0.0.0
ENV UVICORN_ARGS "core.setup:setup_app --host $HOST --port $PORT --workers $UVICORN_WORKERS"

# Settings for PostgresSQL database connections
ENV POSTGRES_DB=""
ENV POSTGRES_USER=""
ENV POSTGRES_PASSWORD=""
ENV POSTGRES_HOST="host.docker.internal"
ENV POSTGRES_PORT=""
ENV POSTGRES_SCHEMA=""

COPY app .

RUN pip install --upgrade pip  --no-cache-dir
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

CMD uvicorn $UVICORN_ARGS
