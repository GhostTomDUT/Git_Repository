 #-*- coding: UTF-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'hard to guess string';
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'KING Admins <2275915852@qq.com>'
    FLASKY_ADMIN = 'xugh93@163.com'
    @staticmethod
    def init2_app():
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER ='smtp.qq.com'
    MAIL_PORT = 25
    MAIL_USE_TLS= True
    MAIL_USERNAME ='2275915852@qq.com'
    MAIL_PASSWORD = 'geidurtsvechebhf'
    SQLALCHEMY_DATABASE_URI ='sqlite:///' + os.path.join(basedir, 'data_dev.sqlite')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI ='sqlite:///' + os.path.join(basedir, 'data_test.sqlite')

class ProductionConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI ='sqlite:///' + os.path.join(basedir, 'data.sqlite')

config = {
    'development':DevelopmentConfig,
    'testing':TestingConfig,
    'production':ProductionConfig,
    'default':DevelopmentConfig
}