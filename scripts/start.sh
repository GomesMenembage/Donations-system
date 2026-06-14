#!/usr/bin/env bash
set -euo pipefail

APP_MODULE="app.main:app"
HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-8000}"
ENVIRONMENT="${ENVIRONMENT:-development}"
WORKERS="${WORKERS:-4}"

if [ "$ENVIRONMENT" = "production" ]; then
    echo "Starting production server on $HOST:$PORT with $WORKERS workers"
    exec gunicorn "$APP_MODULE" \
        --worker-class uvicorn.workers.UvicornWorker \
        --bind "$HOST:$PORT" \
        --workers "$WORKERS" \
        --access-logfile - \
        --error-logfile - \
        --log-level info
else
    echo "Starting development server on $HOST:$PORT with hot reload"
    exec uvicorn "$APP_MODULE" \
        --host "$HOST" \
        --port "$PORT" \
        --reload
fi
