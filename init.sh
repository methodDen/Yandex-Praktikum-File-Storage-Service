#!bin/bash

while ! nc -z $DB_HOST $DB_PORT; do
      echo "Waiting for Postgres..."
      sleep 0.1
done

alembic -c /src/alembic.ini upgrade head

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --workers 1