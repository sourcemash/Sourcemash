export APP_CONFIG_FILE=testing

ps aux | grep 'rss' | awk '{print $2}' | xargs kill

echo "Start Flask app on port 5000..."
python run.py &> flask.log &
FLASK_PID=$!

echo "Run tests...\n"
py.test --boxed tests/

echo "Kill Flask app..."
kill $FLASK_PID

rm test.db