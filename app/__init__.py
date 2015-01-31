import os
from flask import Flask

def create_app(database_url=None):
	app = Flask(__name__, instance_relative_config=True,
				template_folder='frontend/templates',
				static_folder='frontend/static')

	# Load the default configuration
	app.config.from_object('config.default')

	# Load the configuration from the instance folder
	app.config.from_pyfile('config.py', silent=True)

	# Load the file specified by the APP_CONFIG_FILE environment variable
	# Variables defined here will override those in the default configuration
	if 'APP_CONFIG_FILE' in os.environ:
	    app.config.from_object('config.%s' % os.environ.get('APP_CONFIG_FILE'))

	if database_url:
		app.config['SQLALCHEMY_DATABASE_URL'] = database_url

	from app.api import bp as api_bp
	app.register_blueprint(api_bp)

	# SQLAlchemy Database
	from app.database import db, user_datastore, security
	db.init_app(app)
	db.app = app

	security.init_app(app, user_datastore)

	# Frontend Components (Flask-Assets)
	from app.frontend import frontend, assets
	app.register_blueprint(frontend.bp)
	assets.init_app(app)

	return app