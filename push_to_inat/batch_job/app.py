"""
Batch Job App
"""

from aws_cdk import App, Environment

# pylint: disable=no-name-in-module
from stack import BatchJobStack

app = App()

STAGE_NAME = "-".join([
    app.node.try_get_context("namespace"),
    app.node.try_get_context("environment")
])
conf = app.node.try_get_context("environments")[STAGE_NAME]
env = Environment(account=conf["account"], region=conf["region"])
conf['stage'] = STAGE_NAME

stack = BatchJobStack(
    app, '-'.join([STAGE_NAME, conf["name"], "batch-job", "stack"]), conf, env=env
)

app.synth()
