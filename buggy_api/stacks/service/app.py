from aws_cdk import App, Environment

from stack import ServiceStack

app = App(context={"env": "dev"})

conf = app.node.try_get_context("environments")[app.node.try_get_context("env")]
env = Environment(account=conf["account"], region=conf["region"])

stack = ServiceStack(
    app, '-'.join([conf["name"], "service", "stack"]), conf, env=env
)

app.synth()