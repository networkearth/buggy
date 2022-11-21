import click
from aws_cdk import App, Environment

from .stack import BatchJobStack, prefix

@click.command()
@click.option("-e", "--env", required=False, default="buggy_dev")
def main(env):
    # we make sure the cloud stack is there
    app = App(context={"env": env})

    conf = app.node.try_get_context("environments")[app.node.try_get_context("env")]
    env = Environment(account=conf["account"], region=conf["region"])

    stack = BatchJobStack(
        app, '-'.join([prefix(conf), conf['job_name'], 'batch', 'job', 'stack']),
        conf, env=env
    )

    app.synth()
