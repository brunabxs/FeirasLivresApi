''' Módulo responsável por manter as configurações dos diferentes ambientes. '''


class Config(object):
    ''' Configuração padrão '''
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://:memory:'


class ProductionConfig(Config):
    ''' Configuração para ambiente de produção '''
    SQLALCHEMY_DATABASE_URI = 'sqlite:///feiraslivresapi.db'


class TestingConfig(Config):
    ''' Configuração para ambiente de teste '''
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
