import json
import os
from .collections import OrderedSet
import random
import subprocess
from glob import glob
from shutil import rmtree
from shutil import copyfile
class GitValues():
    def __init__(self, namespace, chart, app, colour, envname, region, extra_files=[], extra_values=[]):
        self.namespace = namespace
        self.chart = chart.split('/').pop()
        self.app = app
        self.extra_files = extra_files
        self.extra_values = extra_values
        self.namespace_size = len(self.namespace.split('-', 2))
        self.region = region
        self.colour = colour
        self.envname = envname

    def download_values(self, dest):
        downloaded = []
        if self.region:
            required_files = list(OrderedSet(self.get_all_paths() + self.get_all_paths(self.region)))
        else:
            required_files = self.get_all_paths()

        for extra_values_file in self.extra_values:
            required_files.append(extra_values_file.strip('/'))

        download_path = "/tmp/downloaded_values/{colour}-{envname}-helm-values".format(colour=self.colour, envname=self.envname)
        try:
            rmtree(download_path)
        except:
            pass
        os.makedirs(download_path)
        clone_url = "https://git-codecommit.eu-west-2.amazonaws.com/v1/repos/{colour}-{envname}-helm-values".format(colour=self.colour, envname=self.envname, region=self.region)
        subprocess.check_output(['git', 'clone', clone_url, download_path])

        fileList = self.get_files_as_list(download_path)

        for required_file in required_files:
            if required_file in fileList:
                destination = dest + '/' + required_file
                destination_folder = os.path.dirname(destination)
                if os.path.exists(destination_folder) == False:
                    os.makedirs(destination_folder)
                copyfile(download_path + '/' + required_file, destination)

                downloaded.append(destination)

        return downloaded

    def get_files_as_list(self, download_path):
        results = [y for x in os.walk(download_path) for y in glob(os.path.join(x[0], '*.yaml'))]
        files = []
        for result in results:
            files.append(result.replace(download_path + '/', ''))

        return files

    def get_all_paths(self, root=''):
        paths = []
        path_parts = self.get_path_parts()
        level = 0
        for index, path_part in enumerate(path_parts):
            level += 1
            path = root + '/' + path_part
            path = path.strip('/')
            if level > 0:
                paths.append(path + '/common.yaml')
            if level > 1 and level < self.namespace_size:
                paths.append(path + '/_' + self.chart + '/common.yaml')

            if level > self.namespace_size:
                for extra_file in self.extra_files:
                    extra_file = os.path.splitext(extra_file)[0]
                    paths.append(path + '/' + extra_file + '.yaml')
                paths.append(path + '/' + self.app + '.yaml')

            root = path

        return paths

    def get_path_parts(self):
        parts = self.namespace.split('-', 2)
        parts.append(self.chart)
        parts.append(self.app)
        return parts

