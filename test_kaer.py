import kaer

class TestKaer(object):
    def setup(self):
        self.sd = kaer.SplunkDeployment()

    def test_list_installed_app(self):
        self.sd.list_installed_app()

    def test_list_running_splunk(self):
        self.sd.list_running_splunk()

    def test_list_web_port(self):
        self.sd.list_web_port()

    def test_stop_all_splunk(self):
        self.sd.stop_all_splunk()

