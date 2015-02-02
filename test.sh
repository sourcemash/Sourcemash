# Run all integration and unittests
export APP_CONFIG_FILE=testing

echo "Run unit tests...\n"
py.test --boxed -n10 -k "not functional" tests/

# Run all functional tests
export APP_CONFIG_FILE=selenium

python db_create.py

echo "Start Flask app on port 5000..."
python run.py &> flask.log &
FLASK_PID=$!

echo "Run functional tests...\n"
py.test --boxed tests/test_functional

echo "Kill Flask app..."
kill $FLASK_PIDs

rm "test.db"