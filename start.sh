#!/bin/bash

cd app

# Migrate DB changes
echo Attempting to migrate DB changes
python manage.py migrate

# Collectstatic
if ["$COLLECT_STATIC" == "1"]
then
	echo Collecting Staticfiles
	python manage.py collectstatic --no-input
fi

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn forgyft.wsgi:application \
    --bind 0.0.0.0:80 \
    --workers 2