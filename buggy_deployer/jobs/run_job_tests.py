import click
import json

from subprocess import Popen, PIPE, STDOUT

from .stack import prefix

def run_command(cmd):
    print(cmd)
    with Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT) as process:
        print(process.stdout.read().decode('utf-8'))

@click.command()
@click.option("-e", "--env", required=False, default="ambit_dev")
def main(env):
    print("Running Prep")
    cmd = "./prep.sh"
    run_command(cmd)

    with open("cdk.json", "r") as fh:
        conf = json.load(fh)["context"]["environments"][env]

    container_name = '-'.join([prefix(conf), conf['job_name']])
    print("Building Container...")
    cmd = f"sudo docker build -f Dockerfile -t {container_name} ."
    run_command(cmd)

    region = conf['region']
    print("Running Test...")
    cmd = f"python test.py -c {container_name} -r {region}"
    run_command(cmd)
