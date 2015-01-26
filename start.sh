export APP_CONFIG_FILE=development
echo "Server Running."
echo "To run Celery:"
echo "	redis-server --daemonize yes"
echo "	celery -A worker_tasks.feed_scraper worker --loglevel=debug --beat"
python run.py
