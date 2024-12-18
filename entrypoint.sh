#!/bin/bash
alembic upgrade head && uvicorn main:application --host 0.0.0.0 --port ${PORT} --reload