export APP_CONFIG_FILE=development
redis-server --daemonize yes
python run.py &
celery -A worker_tasks.feed_scraper worker --loglevel=info --beat