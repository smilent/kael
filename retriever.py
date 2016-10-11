import urllib2
import urllib
import threading
import re
import os
from sys import exit, stdout
from common import *
from time import sleep

class Retriever(object):
    def __init__(self, category, name):
        self.url_pattern = 'https://repo.splunk.com/artifactory/Solutions/{category}/{name}/builds/develop/latest/'
        self.category = category
        self.name = name
        
        self.url = self.url_pattern.format(category=self.category, name=self.name)
        self.pkg_pattern = r'<a href="(?P<href>[a-zA-Z0-9_.\-]+.spl)">(?P<name>[a-zA-Z0-9._\-]+)</a>\s+(?P<date>\d{2}-[a-zA-Z]+-\d{4} \d{2}:\d{2})'

        html = self._get_web_content(self.url)
        self.result = self._parse_pkg_html(html)
        

    def _get_web_content(self, url):
        response = urllib2.urlopen(url)
        return response.read()

    def _parse_pkg_html(self, html):
        return re.search(self.pkg_pattern, html)

    def get_latest_pkg_url(self):
        return self.url + self.result.group('href')

    def get_latest_pkg_name(self):
        return self.result.group('name')

    def get_latest_pkg_date(self):
        return self.result.group('date')

    def download_latest_pkg(self):
        if self.category == 'APP':
            path = config['app_path']
        elif self.category == 'TA':
            path = config['ta_path']
        elif self.category == 'SA':
            path = config['sa_path']
        else:
            print self.category + ' download path not found in config'
            exit()

        if not os.path.exists(path):
            os.makedirs(path)
        
        pkg_dir = os.path.join(path, self.name)
        if not os.path.exists(pkg_dir):
            os.makedirs(pkg_dir)

        pkg_path = os.path.join(pkg_dir, self.get_latest_pkg_name())
        if os.path.exists(pkg_path):
            pass
        else:
            t = threading.Thread(name='download', target = lambda : urllib.urlretrieve(self.get_latest_pkg_url(), pkg_path))
            t.start()
            stdout.write('downloading ')
            while t.isAlive():
                sleep(1)
                stdout.write('.')
                stdout.flush()
            stdout.write('\nfinish\n')
            stdout.flush()

        return pkg_path

