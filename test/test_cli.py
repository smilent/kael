import subprocess

class TestCLI(object):
    def test_list_web_port(self):
        p = subprocess.Popen(['kael', '--log=debug', 'list', '-wp'], stderr=subprocess.PIPE)
        p.wait()
        out, err = p.communicate()
        assert err == ''

    def test_list_running_splunkt(self):
        p = subprocess.Popen(['kael', '--log=debug', 'list', '-rs'], stderr=subprocess.PIPE)
        p.wait()
        out, err = p.communicate()
        assert err == ''


    def test_list_installed_app(self):
        p = subprocess.Popen(['kael', '--log=debug', 'list', '-ia'], stderr=subprocess.PIPE)
        p.wait()
        out, err = p.communicate()
        assert err == ''

    def test_latest(self):
        p = subprocess.Popen(['kael', '--log=debug', 'latest', '-app', 'aws', '-d'], stderr=subprocess.PIPE)
        p.wait()
        out, err = p.communicate()
        assert err == ''

    def test_update(self):
        p = subprocess.Popen(['kael', '--log=debug', 'update', 'splunk-ivory-aws', '-app', 'aws', '-r'], stderr=subprocess.PIPE)
        p.wait()
        out, err = p.communicate()
        assert err == ''
