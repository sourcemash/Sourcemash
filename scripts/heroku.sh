gunicorn sourcemash:create_app\(\) --daemon
python manage.py scrape_worker &
python manage.py user_tasks_worker &
python manage.py scrape_loop
