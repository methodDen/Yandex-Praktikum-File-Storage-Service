#!/bin/bash
sleep 2

echo "running migrations"
alembic upgrade head

sleep 2

echo "starting app"
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload --workers 1