import click
import json

from subprocess import Popen, PIPE, STDOUT

from .stack import prefix

def run_command(cmd):
    print(cmd)
    with Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT) as process:
        print(process.stdout.read().decode('utf-8'))

@click.command()
@click.option("-e", "--env", required=False, default="buggy_dev")
def main(env):
    with open("cdk.json", "r") as fh:
        conf = json.load(fh)["context"]["environments"][env]

    container_name = '-'.join([prefix(conf), conf['job_name']])
    print("Building Container...")
    cmd = f"docker build --build-arg AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID --build-arg AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY --build-arg AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION --platform linux/amd64 -f Dockerfile -t {container_name} ."
    run_command(cmd)

    region = conf['region']
    print("Running Test...")
    cmd = f"python test.py -c {container_name} -r {region}"
    run_command(cmd)
