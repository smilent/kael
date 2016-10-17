__author__ = 'Jarvis'

# this modular wraps some common function and class

import string
import os
from os.path import isdir
from os.path import isfile
from os.path import join

import logging

logger = logging.getLogger(__name__)

DEFAULT_CONFIG_FILE = join(os.path.dirname(os.path.abspath(__file__)), 'default.conf')
LOCAL_CONFIG_FILE = join(os.path.dirname(os.path.abspath(__file__)), 'local.conf')

class Config(object):
    class _Config:
        def __init__(self):
            self.config = {}
            self._load_config()

        def _load_config(self):
            # load default config
            if os.path.exists(DEFAULT_CONFIG_FILE):
                with open(DEFAULT_CONFIG_FILE, 'r') as infile:
                    for config in infile:
                        if '=' not in config:
                            continue
                        key, value = string.split(config, '=')
                        self.config[string.strip(key)] = string.strip(value)

            # load local config and overwrite default config if a key already existed
            if os.path.exists(LOCAL_CONFIG_FILE):
                with open(LOCAL_CONFIG_FILE, 'r') as infile:
                    for config in infile:
                        if '=' not in config:
                            continue
                        key, value = string.split(config, '=')
                        self.config[string.strip(key)] = string.strip(value)
	    
	    logger.debug(self.config)


        def get_config(self):
            return self.config

    instance = None

    def __new__(cls):
        if not Config.instance:
            Config.instance = Config._Config()
            logging.info('create Config instance')
            logging.debug('config: ' + str(Config.instance.get_config()))
        return Config.instance

def is_splunk_dir(path):
    return isdir(path) and isdir(join(path, 'bin')) and isfile(join(path, 'bin/splunk'))

