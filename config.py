class Config:
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:pass123@localhost/api'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:pass123@localhost/api_test'
    SQLALCHEMY_TRACK_MODIFICATIONS = False   

config = {
    'test': TestConfig,
    'development': DevelopmentConfig
}