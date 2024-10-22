#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi
git pull
export DJANGO_SETTINGS_MODULE=travel_verse.settings
python manage.py migrate
python manage.py collectstatic --no-input
gunicorn -w 7 -b 0.0.0.0:8000 Product.wsgi --reload


exec "$@"