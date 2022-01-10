#!/bin/bash

gunicorn --bind :$FASTAPI_PORT --workers 1 --threads 8 --timeout 0 -k uvicorn.workers.UvicornH11Worker app.main:app
