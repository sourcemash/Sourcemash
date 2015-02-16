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
SECURITY_POST_LOGIN_VIEW = "/profile"
SECURITY_POST_REGISTER_VIEW = "/profile"
SECURITY_POST_LOGOUT_VIEW = "/login"
SECURITY_REGISTERABLE = True
SECURITY_SEND_REGISTER_EMAIL = False

SECURITY_MSG_INVALID_PASSWORD = ("Invalid username/password combination", "error")
SECURITY_MSG_PASSWORD_NOT_PROVIDED = ("Invalid username/password combination", "error")
SECURITY_MSG_USER_DOES_NOT_EXIST = ("Invalid username/password combination", "error")

logging.basicConfig(level=logging.DEBUG)

logging.info("Default settings loaded.")
