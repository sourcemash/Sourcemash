. flask/bin/activate
export APP_CONFIG_FILE=testing
nosetests --nocapture
deactivate