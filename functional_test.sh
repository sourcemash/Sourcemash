# Run all functional tests
export APP_CONFIG_FILE=selenium

python db_create.py

echo "Start Flask app on port 5000..."
python manage.py server &> flask.log &
FLASK_PID=$!

echo "Run functional tests..."
py.test --boxed tests/test_functional

echo "Kill Flask app..."
kill $FLASK_PIDs

rm "test.db"