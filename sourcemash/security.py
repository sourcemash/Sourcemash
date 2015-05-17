from rq import Queue
from flask.ext.security import SQLAlchemyUserDatastore, Security
from sourcemash.models import User, Role
from sourcemash.database import db
from sourcemash.mail import send_security_email
from worker import create_worker

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security()
REDIS_CONNECTION = create_worker()


def delay_security_email(msg):
    q = Queue('email', connection=REDIS_CONNECTION)
    q.enqueue_call(func=send_security_email, args=(msg,),
                   at_front=True, timeout=600)
