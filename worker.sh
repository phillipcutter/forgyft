#!/bin/bash

cd app

# Start Gunicorn processes
echo Starting Worker.
exec celery -A forgyft worker -l info