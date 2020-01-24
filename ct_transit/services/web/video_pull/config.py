import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = 'hard to guess string'
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
#app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
#app.config['MAIL_PORT'] = 587
#app.config['MAIL_USE_TLS'] = True
#app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
#app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
