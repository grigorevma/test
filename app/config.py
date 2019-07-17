import os

basedir = os.path.abspath(os.path.dirname(__file__))

currencies = {
    "EUR": 978,
    "USD": 840,
    "RUB": 643
}

Secret_to_piastrix = "SecretKey01"
SHOP_ID = "5"
PAY_WAY = "card_rub"


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[Admin]'
    FLASKY_MAIL_SENDER = 'Admin <flasky@example.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
                'development': DevelopmentConfig,
                'testing': TestingConfig,
                'production': ProductionConfig,
                'default': DevelopmentConfig
            }
