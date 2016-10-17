from common import *
from os.path import isfile
import splunk_deployment
import logging

logger = logging.getLogger(__name__)

splunk_deployment = splunk_deployment.SplunkDeployment()

def info(args):
    splunk = splunk_deployment.get_splunk(args['splunk'])

    if args['app']:
        app_conf_path = '{splunk_path}/etc/apps/{app}/default/app.conf'.format(splunk_path=splunk.get_path(),app=args['app'])
        if isfile(app_conf_path):
            with open(app_conf_path, 'r') as infile:
                for line in infile:
                    if '=' in line:
                        key, value = string.split(line, '=')
                        if 'build' == string.strip(key):
                            build = string.strip(value)

                        if 'version' == string.strip(key):
                            version = string.strip(value)
                        
            print 'version: {version}, build: {build}'.format(version=version, build=build)
        else:
            print args['app'] + ' does not exist'
    else:
        out, err = splunk.run_command(['version'])
        if err == '':
            print out
        else:
            print "can't get info of {splunk}".format(splunk=splunk.get_name())
            logger.error(err)
            exit()
