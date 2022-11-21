import os
import click
import boto3
import json
import pandas as pd

from time import time
from subprocess import Popen, PIPE, STDOUT

@click.command()
@click.option('-c', '--container', required=True, help='name of the container to run')
@click.option('-r', '--region', required=True, help='the aws region')
def main(container, region):
    
    cmd = f'sudo docker run {container} {partition} {environment} {carriers_table} {contour_info_table} {bucket} {region}'
    print('running:', cmd)
    with Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT) as process:
        print(process.stdout.read().decode('utf-8'))

if __name__ == '__main__':
    main()