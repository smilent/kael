__author__ = 'Jarvis'

# this moduler checks splunk deployment environment and wrap splunk cli commands

import os
import subprocess
from os.path import isdir
from os.path import isfile
from os.path import join
from common import *
import logging

logger = logging.getLogger(__name__)

config = Config().get_config()

class SplunkDeployment(object):
    class _Splunk(object):
        def __init__(self, name, full_path):
            self.name = name
            self.path = full_path

        def get_name(self):
            return self.name

        def get_path(self):
            return self.path

        def run_command(self, command, stdout=subprocess.PIPE, stderr=subprocess.PIPE):
            return SplunkDeployment.instance._run_command(self.name, command, stdout, stderr)


    class _SplunkDeployment:
        def __init__(self):
            self.splunk_deployment_path = config['splunk_deployment_path']

            self.splunk_instances = {}
            for ele in os.listdir(self.splunk_deployment_path):
                full_path = join(self.splunk_deployment_path, ele)
                if is_splunk_dir(full_path):
                    self.splunk_instances[str(ele)] = SplunkDeployment._Splunk(ele, full_path)

            logger.info('found splunks: {splunks}'.format(splunks=self.splunk_instances.keys()))

        def list_installed_app(self):
            command = ['display', 'app']
            for splunk in self.splunk_instances.values():
                out, err = splunk.run_command(command)
                print splunk.get_name() + ':'
                for app in self._filter_app(out):
                    print app
                print '===================================================='

        def list_running_splunk(self):
            command = ['status']
            for splunk in self.splunk_instances.values():
                out, err = splunk.run_command(command)

                if 'is running' in out:
                    print splunk.get_name()

        def list_web_port(self):
            command = ['show', 'web-port']
            for splunk in self.splunk_instances.values():
                out, err = splunk.run_command(command)

                if 'Web port' in out:
                    port = string.strip(string.split(out,':')[1])
                    print splunk.get_name() + ':' + port 

        def stop_all_splunk(self):
            command = ['stop']
            for splunk in self.splunk_instances.values():
                out, err = splunk.run_command(['status'])
                if 'is running' in out:
                    print 'stopping ' + splunk.get_name()
                    self._run_command(splunk.get_name(), command)
    
        def get_splunk(self, name):
            if name in self.splunk_instances.keys():
                return self.splunk_instances[name]
            else:
                logger.error('splunk {name} does not exist in path {path}'.format(name=name, path=self.splunk_deployment_path))
                print 'splunk {splunk} does not exist'.format(splunk=name)
                exit()

        def _run_command(self, splunk, command, stdout=subprocess.PIPE, stderr=subprocess.PIPE):
            c = [join(self.get_splunk(splunk).get_path(), 'bin/splunk')]
            c.extend(command)
            logger.info('running: {command}'.format(command = str(c)))
            p = subprocess.Popen(c, stdout=stdout, stderr=stderr)
            p.wait()
            return p.communicate()

        def _get_splunk_deployment_path(self):
            return self.splunk_deployment_path

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

