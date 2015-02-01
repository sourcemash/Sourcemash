export APP_CONFIG_FILE=testing

echo "Run tests...\n"
py.test --boxed tests/

rm test.db