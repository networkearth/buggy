"""
Container App
"""

from aws_cdk import App, Environment

# pylint: disable=no-name-in-module
from stack import ContainerStack

app = App()

STAGE_NAME = "-".join([
    app.node.try_get_context("namespace"),
    app.node.try_get_context("environment")
])
conf = app.node.try_get_context("environments")[STAGE_NAME]
env = Environment(account=conf["account"], region=conf["region"])
conf['stage'] = STAGE_NAME

stack = ContainerStack(
    app, '-'.join([STAGE_NAME, conf["name"], "container", "stack"]), conf, env=env
)

app.synth()
