#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

import sys
import argparse
import subprocess
import re
from common import *

def list_scheduled_searches(splunk_dir, app):
    command = '| rest /servicesNS/nobody/{app}/saved/searches| search is_scheduled=1 disabled=0| table title '.format(app=app)
    p = subprocess.Popen([join(splunk_dir,'bin/splunk'), 'search', command], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    p.wait()
    result = p.communicate()[0]
    if result:
        searches = result.split('\n')[2:-1]
    return searches

def run_search(splunk_dir, app, search):
    command = '|savedsearch "{search}" |stats count'.format(search=search)
    p = subprocess.Popen([join(splunk_dir, 'bin/splunk'), 'search', command, '-app', app], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    p.wait()
    #print p.communicate()
    result = p.communicate()[0]
    pattern = r'\d+'
    m = re.search(pattern, result)

    print 'Complete ' + search
    print 'Find ' + m.group() + ' results'


if __name__ == '__main__':
    splunk_name = sys.argv[1]
    splunk_path = config['splunk_path']
    splunk_dir = join(splunk_path, splunk_name)
    if not is_splunk_dir(splunk_dir):
        print splunk_name + ' does not exist'
        exit()
    app = sys.argv[2]

    searches = list_scheduled_searches(splunk_dir, app)
    print 'Find {0} searches'.format(len(searches))
    print '---------------------------------------'

    for search in searches:
        run_search(splunk_dir, app, search)

