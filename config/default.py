import os
import logging

basedir = os.path.abspath(os.path.dirname('run.py'))

DEBUG = False

SECRET_KEY = 'thisisnearlyimpossible'

WTF_CSRF_ENABLED = False

SQLALCHEMY_DATABASE_URI = ('sqlite:///' + os.path.join(basedir, 'app.db'))

# Flask security config variables- https://pythonhosted.org/Flask-Security/configuration.html
SECURITY_FLASH_MESSAGES = True
SECURITY_PASSWORD_HASH = "bcrypt"
SECURITY_PASSWORD_SALT = "abcde1234509876zyxwvu22"
SECURITY_REGISTER_USER_TEMPLATE = "index.html"
SECURITY_LOGIN_USER_TEMPLATE = "index.html"
SECURITY_FORGOT_PASSWORD_TEMPLATE = "index.html"
SECURITY_POST_LOGOUT_VIEW = "/"
SECURITY_EMAIL_SUBJECT_REGISTER = "Welcome to Sourcemash!"
SECURITY_REGISTERABLE = True
SECURITY_RECOVERABLE = True
SECURITY_LOGIN_WITHOUT_CONFIRMATION = True
SECURITY_SEND_REGISTER_EMAIL = False

SECURITY_MSG_INVALID_PASSWORD = ("Invalid username/password combination", "error")
SECURITY_MSG_PASSWORD_NOT_PROVIDED = ("Invalid username/password combination", "error")
SECURITY_MSG_USER_DOES_NOT_EXIST = ("Invalid username/password combination", "error")

SECURITY_EMAIL_SENDER = "support@sourcemash.com"

# Email Server
ADMINS = ['admin@sourcemash.com', 'support@sourcemash.com']

MAIL_SERVER = 'mail.privateemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

logging.basicConfig(level=logging.WARNING)

logging.getLogger("requests").setLevel(logging.WARNING)

logger = logging.getLogger('Sourcemash')
logger.setLevel(logging.INFO)

logger.info("Default settings loaded.")
