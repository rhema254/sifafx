from decouple import config

class Config():
    SQLALCHEMY_ECHO = True
    SECRET_KEY = config('SECRET_KEY')
    # CLIENT_SECRETS_FILE = config('CLIENT_SECRETS_FILE')
    # SCOPES = 'https://www.googleapis.com/auth/calendar.events'
    
class DevConfig(Config):
    DB_HOST = config('DB_HOST')
    DB_USERNAME = config('DB_USERNAME')
    DB_PASSWORD = config('DB_PASSWORD')
    DB_NAME = config('DB_NAME')
    SQLALCHEMY_DATABASE_URI = config('DB_CONNECTION_STRING')
    MAIL_SERVER = config('MAIL_SERVER')
    MAIL_PORT = 465
    
    MAIL_USERNAME = config('MAIL_USERNAME')
    MAIL_PASSWORD= config('MAIL_PASSWORD')

class TestConfig(Config):
    pass

class ProdConfig(Config):
    pass 

 