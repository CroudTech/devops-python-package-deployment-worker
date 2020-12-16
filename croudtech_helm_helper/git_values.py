import json
import os
from .collections import OrderedSet
import random
import subprocess
from glob import glob
from shutil import rmtree
from shutil import copyfile
import boto3
from botocore.exceptions import ClientError
import click

class GitValues:
    def __init__(
        self,
        namespace,
        chart,
        app,
        colour,
        envname,
        region,
        extra_files=[],
        extra_values=[],
        ssm_prefix="/devops/pipeline/"
    ):
        self.namespace = namespace
        self.chart = chart.split("/").pop()
        self.app = app
        self.extra_files = extra_files
        self.extra_values = extra_values
        self.namespace_size = len(self.namespace.split("-", 2))
        self.region = region
        self.colour = colour
        self.envname = envname
        self.ssm_prefix = ssm_prefix

    def download_values(self, dest):
        downloaded = []
        if self.region:
            required_files = list(
                OrderedSet(self.get_all_paths() + self.get_all_paths(self.region))
            )
        else:
            required_files = self.get_all_paths()

        for extra_values_file in self.extra_values:
            required_files.append(extra_values_file.strip("/"))

        download_path = "tmp/downloaded_values/{colour}-{envname}-helm-values".format(
            colour=self.colour, envname=self.envname
        ).replace("/", os.path.sep)
        try:
            rmtree(download_path)
        except:
            pass
        os.makedirs(download_path)

        subprocess.check_output(["git", "clone", "--depth=1", self.clone_url, download_path])

        fileList = self.get_files_as_list(download_path)

        for required_file in required_files:
            if required_file in fileList:
                destination = dest + os.path.sep + required_file
                destination_folder = os.path.dirname(destination)
                if os.path.exists(destination_folder) == False:
                    os.makedirs(destination_folder)
                copyfile(download_path + os.path.sep + required_file, destination)

                downloaded.append(destination)

        return downloaded

    @property
    def ssm_client(self):
        if not hasattr(self, '_ssm_client'):
            self._ssm_client = boto3.client('ssm')

        return self._ssm_client

    def get_ssm_value(self, key, default=None, with_decryption=False):
        attr_name = "_%s" % key

        if not hasattr(self, attr_name):
            try:
                ssm_path = self.ssm_prefix + key
                print(ssm_path)

                response = self.ssm_client.get_parameter(
                    Name=ssm_path,
                    WithDecryption=with_decryption
                )
                setattr(self, attr_name, response['Parameter']['Value'])
            except ClientError as e:
                if e.__class__.__name__ == 'ParameterNotFound':
                    return default
                raise e

        return getattr(self, attr_name)

    @property
    def repository_source(self):
        return self.get_ssm_value('repository_source', 'codecommit')

    @property
    def github_pat(self):
        return self.get_ssm_value('github_pat', with_decryption=True)

    @property
    def clone_url(self):
        if self.repository_source == 'github':
            click.echo(click.style('Using GitHub', fg="green", bold=True))
            return "https://{github_pat}@github.com/CroudTech/{colour}-{envname}-helm-values.git".format(
                colour=self.colour, envname=self.envname, region=self.region, github_pat=self.github_pat
            )
        else:
            click.echo(click.style('Using CodeCommit', fg="green", bold=True))
            return "https://git-codecommit.eu-west-2.amazonaws.com/v1/repos/{colour}-{envname}-helm-values".format(
                colour=self.colour, envname=self.envname, region=self.region
            )

    def get_files_as_list(self, download_path):
        results = [
            y
            for x in os.walk(download_path)
            for y in glob(os.path.join(x[0], "*.yaml"))
        ]
        files = []
        for result in results:
            files.append(result.replace(download_path + os.path.sep, ""))

        return files

    def get_all_paths(self, root=""):
        paths = []
        path_parts = self.get_path_parts()
        level = 0
        for index, path_part in enumerate(path_parts):
            level += 1
            path = root + os.path.sep + path_part
            path = path.strip(os.path.sep)
            if level > 0:
                paths.append(path + os.path.sep + "common.yaml")
                paths.append(path + os.path.sep + "_system.yaml")
            if level > 1 and level < self.namespace_size:
                paths.append(path + os.path.sep + "_" + self.chart + os.path.sep + "common.yaml")
                paths.append(path + os.path.sep + "_" + self.chart + os.path.sep + "_system.yaml")

            if level > self.namespace_size:
                for extra_file in self.extra_files:
                    extra_file = os.path.splitext(extra_file)[0]
                    paths.append(path + os.path.sep + extra_file + ".yaml")
                paths.append(path + os.path.sep + self.app + ".yaml")

            root = path

        return paths

    def get_path_parts(self):
        parts = self.namespace.split("-", 2)
        parts.append(self.chart)
        parts.append(self.app)
        return parts
