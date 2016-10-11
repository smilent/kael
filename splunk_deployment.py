import os
import subprocess
from os.path import isdir
from os.path import isfile
from os.path import join

from common import *

class SplunkDeployment(object):
    class _SplunkDeployment:
        def __init__(self):
            self.splunk_path = config['splunk_path']
            self.splunk_dirs = [d for d in os.listdir(self.splunk_path) if is_splunk_dir(join(self.splunk_path, d))]

        def _command_wrapper(self, path, command):
            c = [join(join(self.splunk_path, path), 'bin/splunk')]
            c.extend(command)
            p = subprocess.Popen(c, stdout = subprocess.PIPE)
            p.wait()
            return p.communicate()

        def list_installed_app(self):
            command = ['display', 'app']
            for ele in self.splunk_dirs:
                out, err = self._command_wrapper(ele, command)
                print ele + ':'
                for app in self._filter_app(out):
                    print app
                print '===================================================='

        def list_running_splunk(self):
            command = ['status']
            for ele in self.splunk_dirs:
                out, err = self._command_wrapper(ele, command)

                if 'is running' in out:
                    print ele

        def list_web_port(self):
            command = ['show', 'web-port']
            for ele in self.splunk_dirs:
                out, err = self._command_wrapper(ele, command)

                if 'Web port' in out:
                    port = string.strip(string.split(out,':')[1])
                    print ele + ':' + port 

        def stop_all_splunk(self):
            command = ['stop']
            for ele in self.splunk_dirs:
                out, err = self._command_wrapper(ele, ['status'])
                if 'is running' in out:
                    print 'stopping ' + ele
                    self._command_wrapper(ele, command)

        def _filter_app(self, apps):
            preinstalled_apps = ['alert_logevent',
                    'alert_webhook',
                    'appsbrowser',
                    'framework',
                    'gettingstarted',
                    'introspection_generator_addon',
                    'launcher',
                    'learned',
                    'legacy',
                    'sample_app',
                    'search',
                    'splunk_archiver',
                    'splunk_httpinput',
                    'splunk_instrumentation'
                    'splunk_monitoring_console',
                    'SplunkForwarder',
                    'SplunkLightForwarder']

            all_apps = string.split(apps, '\n')
            installed_apps = []
            for app in all_apps:
                if app and string.split(app)[0] not in preinstalled_apps:
                    installed_apps.append(app)

            return installed_apps


    instance = None

    def __new__(cls):
        if not SplunkDeployment.instance:
            SplunkDeployment.instance = SplunkDeployment._SplunkDeployment()

        return SplunkDeployment.instance
