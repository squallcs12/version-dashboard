web: gunicorn version_dashboard.wsgi --log-file -
worker: celery worker -A version_dashboard -l info
release: python manage.py heroku_release
