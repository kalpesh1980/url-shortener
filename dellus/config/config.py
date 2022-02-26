import os

from configparser import ConfigParser, NoSectionError

_CONFIG_ENV_VAR = 'DELLUS_CONFIG_FILE'


class Configuration:
    def __init__(self):       
        self.default_config_path = 'dellus/config/dellus.cfg'
        self.cfg = None
        self.debug = False
        self.schema = None
        self.host = None
        self.port = None
        self.secret = None
        self.logging = None
        self.webservice_url = None
        self.database = None
        self.initialize()

    def _read_cfg(self):
        self.cfg = ConfigParser()
        self.cfg.read(os.environ.get(_CONFIG_ENV_VAR, self.default_config_path))

    def __getattr__(self, name):
       
        if self.cfg is None:
            self._read_cfg()
        try:
            return dict(self.cfg[name].items())
        except KeyError:
            return NoSectionError('No {} section found'.format(name))

    def initialize(self):
       
        self._read_cfg()
        self.debug = (self.cfg['dellus']['debug'] == 'True')
        self.database = dict(self.cfg['database'].items())
        self.schema = self.cfg['dellus']['schema']
        self.host = self.cfg['dellus']['host']
        self.port = self.cfg['dellus']['port']
        self.secret = self.cfg['dellus']['flask_secret']
        self.logging = self.cfg['logging']
        self.webservice_url = "{0}://{1}:{2}".format(
            self.schema, self.host, self.port)  
