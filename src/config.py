from configparser import ConfigParser
from utils import str_to_bool
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    CONFIG_FILENAME = 'config.ini'
    JSON_RECORD_LIMIT = 1000
    PRETTY_PRINT = 4
    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or 'Z3kDutZBDBa84hHzsofFqT8GPM78LOfZpYgMbAWyKDxFKqX5kBBG5k2Lf7KvzgOx07yLSA9mnPweWz+pZqQ7VQ=='
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        print("Config init app {}".format(app.name))


class DevConfig(Config):
    CONFIG_SECTION = 'dev'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'kros-dev.sqlite')

    def __init__(self):
        config_path = os.path.join(BASE_DIR, self.CONFIG_FILENAME)
        config = ConfigParser()
        if config.read(config_path):
            if config.has_option(self.CONFIG_SECTION, "url"):
                self.SQLALCHEMY_DATABASE_URI = config.get(
                    self.CONFIG_SECTION, "url")
            if config.has_option(self.CONFIG_SECTION, "debug"):
                self.DEBUG = str_to_bool(
                    config.get(self.CONFIG_SECTION, "debug"))


class ProConfig(Config):
    CONFIG_SECTION = 'pro'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'kros-pro.sqlite')

    def __init__(self):
        config_path = os.path.join(BASE_DIR, self.CONFIG_FILENAME)
        config = ConfigParser()
        if config.read(config_path):
            if config.has_option(self.CONFIG_SECTION, "url"):
                self.SQLALCHEMY_DATABASE_URI = config.get(
                    self.CONFIG_SECTION, "url")
            if config.has_option(self.CONFIG_SECTION, "debug"):
                self.DEBUG = str_to_bool(
                    config.get(self.CONFIG_SECTION, "debug"))


CONFIG = {
    'dev': DevConfig(),
    'pro': ProConfig(),
    'default': DevConfig()
}
