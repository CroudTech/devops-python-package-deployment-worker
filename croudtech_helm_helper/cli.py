import json
import click
import os
from .git_values import GitValues
from pathlib import Path
import ruamel.yaml
yaml = ruamel.yaml.YAML()

@click.command()
@click.option('--namespace', default="default", help='The namespace for the release')
@click.option('--chart', default="nginx", help='The name of the chart')
@click.option('--app', required="true", help='The app name for the release')
@click.option('--extrafiles', help='Extra file names to search for')
@click.option('--extravalues', help='Full paths to extra values files')
@click.option('--destination', default="/tmp", help='The destination for downloaded values files')
@click.option('--output', required="true", default='json', help='The source s3 bucket name', type=click.Choice(['json', 'helm', 'combined']))
@click.option('--region', default="eu-west-2", help='The target region')
@click.option('--envname', default="development", help='The target environment')
@click.option('--colour', default="blue", help='The target colour')
def main(namespace, chart, app, extrafiles, extravalues, destination, output, region, envname, colour):
    """Build all possible s3 paths for values files"""
    if extrafiles == None:
        extrafiles = []
    else:
        extrafiles = extrafiles.split(',')
    if extravalues == None:
        extravalues = []
    else:
        extravalues = extravalues.split(',')

    bp = GitValues(namespace, chart, app, region, extrafiles, extravalues)
    bp = GitValues(
        namespace=namespace,
        chart=chart,
        app=app,
        colour=colour,
        envname=envname,
        region=region,
        extra_files=extrafiles,
        extra_values=extravalues
    )

    downloaded = bp.download_values(destination)
    if output == 'json':
        print(json.dumps(downloaded))
    elif output == 'combined':
        combined = {}
        for file in downloaded:
            with open(file) as fp:
                data = yaml.load(fp)
                combined.update(data)
        filename = destination + '/combined-%s-%s.yaml' % (namespace, app)
        fout = open(filename, 'w+')
        yaml.dump(combined, fout)
        fout.close()
        print(filename)
    elif output == 'helm':
        helm_args = ''
        for file in downloaded:
            helm_args = helm_args + ' --values ' + file
        print(helm_args)



if __name__ == '__main__':
    main()
