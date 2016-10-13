from common import *

class TestConfig(object):
    def setup(self):
        self.config = Config().get_config()

    def test_config(self):
        print self.config
