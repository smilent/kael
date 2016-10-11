import string
import os
from os.path import isdir
from os.path import isfile
from os.path import join

CONFIG_FILE = join(os.path.dirname(os.path.abspath(__file__)),'config.conf')

class Config(object):
    class _Config:
        def __init__(self):
            self.config = {}
            self._load_config(CONFIG_FILE)

        def _load_config(self,config_file):
            with open(config_file, 'r') as infile:
                for config in infile:
                    if '=' not in config:
                        continue
                    key, value = string.split(config, '=')
                    self.config[string.strip(key)] = string.strip(value)

        def get_config(self):
            return self.config

    instance = None

    def __new__(cls):
        if not Config.instance:
            Config.instance = Config._Config()
        return Config.instance


config = Config().get_config()

def is_splunk_dir(path):
    return isdir(path) and isdir(join(path, 'bin')) and isfile(join(path, 'bin/splunk'))

