import logging

DEBUG = True
SQLALCHEMY_ECHO = True

SECURITY_SEND_REGISTER_EMAIL = False

MAIL_SERVER = 'mail.privateemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True

logger = logging.getLogger('Sourcemash')
logger.setLevel(logging.DEBUG)

logger.info("Development settings loaded.")
