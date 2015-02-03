from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import SQLAlchemyUserDatastore, Security
from flask.ext.migrate import Migrate

db = SQLAlchemy()
from models import User, Role
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security()
migrate = Migrate()