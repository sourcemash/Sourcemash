from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import SQLAlchemyUserDatastore, Security

db = SQLAlchemy()
from models import User, Role
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security()