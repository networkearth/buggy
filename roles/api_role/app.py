from aws_cdk import App, Environment

from stack import BucketStack

app = App(context={"env": "dev"})

conf = app.node.try_get_context("environments")[app.node.try_get_context("env")]
env = Environment(account=conf["account"], region=conf["region"])

stack = BucketStack(
    app, '-'.join([conf["name"], "container", "stack"]), conf, env=env
)

app.synth()