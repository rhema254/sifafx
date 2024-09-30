from decouple import config

class Config():
    SECRET_KEY = config('SECRET_KEY')
    # CLIENT_SECRETS_FILE = config('CLIENT_SECRETS_FILE')
    # SCOPES = 'https://www.googleapis.com/auth/calendar.events'
    
class DevConfig(Config):
    DB_HOST = config('DB_HOST')
    DB_USERNAME = config('DB_USERNAME')
    DB_PASSWORD = config('DB_PASSWORD')
    DB_NAME = config('DB_NAME')
    DB_CONNECTION_STRING = config('DB_CONNECTION_STRING')

class TestConfig(Config):
    pass

class ProdConfig(Config):
    pass 

 