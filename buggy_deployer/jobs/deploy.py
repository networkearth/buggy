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
    print("Running CDK Deploy...")
    cmd = f"cdk deploy -c env={env} --profile=deployer"
    run_command(cmd)

    with open("cdk.json", "r") as fh:
        conf = json.load(fh)["context"]["environments"][env]

    print("Logging Into Docker Hub")
    cmd = f"aws ecr get-login-password --region {conf['region']} | sudo docker login --username AWS --password-stdin {conf['account']}.dkr.ecr.{conf['region']}.amazonaws.com"
    run_command(cmd)

    print("Building Container...")
    cmd = f"sudo docker build -f Dockerfile -t {prefix(conf)}-{conf['job_name']} ."
    run_command(cmd)

    print("Tagging Container...")
    cmd = f"sudo docker tag {prefix(conf)}-{conf['job_name']}:latest {conf['account']}.dkr.ecr.{conf['region']}.amazonaws.com/{prefix(conf)}-{conf['job_name']}:latest"
    run_command(cmd)

    print("Pushing Container...")
    cmd = f"sudo docker push {conf['account']}.dkr.ecr.{conf['region']}.amazonaws.com/{prefix(conf)}-{conf['job_name']}:latest"
    run_command(cmd)
