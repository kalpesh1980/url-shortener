import sys
import os

from dellus.config import config
from dellus.database.factory import DatabaseFactory

_CONFIG_ENV_VAR = 'DELLUS_CONFIG_FILE'
_CFG_PATHS = ['dellus/config/dellus.cfg', 'dellus.cfg',
              '$HOME/.dellus.cfg', '/etc/dellus.cfg']


def load_config_path(config_path=None):
    if config_path and os.path.exists(config_path):
        os.environ[_CONFIG_ENV_VAR] = config_path
        return
    for cfg_path in _CFG_PATHS:
        if os.path.exists(cfg_path):
            os.environ[_CONFIG_ENV_VAR] = cfg_path
            break


def initialize_config(config_path=None):
    os.environ['TZ'] = 'UTC'
    if config_path and os.path.exists(config_path):
        os.environ[_CONFIG_ENV_VAR] = config_path
    else:
        load_config_path(config_path)
    if os.environ.get(_CONFIG_ENV_VAR) is None:
        print('\nNo _CONFIG_ENV_VAR variable set. Exiting...')
        sys.exit(1)
    config.initialize()


def initialize_db():
    database = DatabaseFactory()
    config.db = database.create()


def initialize(config_path=None):
    initialize_config(config_path)
    initialize_db()


def initialize_test(config_path=None, db_url=None):
    """For handeling initialization while running tests"""
    initialize_config(config_path)  
    initialize_db()
