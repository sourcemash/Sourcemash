gunicorn sourcemash:create_app\(\) --daemon
python manage.py worker &
python manage.py scrape
