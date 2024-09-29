from decouple import config

class Config():
    SECRET_KEY = config('SECRET_KEY')
    # CLIENT_SECRETS_FILE = config('CLIENT_SECRETS_FILE')
    # SCOPES = 'https://www.googleapis.com/auth/calendar.events'
    
class DevConfig(Config):
    pass

class TestConfig(Config):
    pass

class ProdConfig(Config):
    pass 

 