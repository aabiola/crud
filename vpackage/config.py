'''To enable any config defined here, you just have to call into from_object():'''
# app.config.from_object('configmodule.ProductionConfig') Example: app.config.from_object('config.ProductionConfig')


class Config(object):
    '''base class'''
    DEBUG = False
    TESTING = False
    #DATABASE_URI = 'mysql+mysqlconnector://root:@localhost/orm'

class ProductionConfig(Config): 
    #DATABASE_URI = 'mysql://user@localhost/foo'
    TESTING = True

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True