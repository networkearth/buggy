from aws_cdk import App, Environment

from stack import UserStack

app = App(context={"env": "dev"})

conf = app.node.try_get_context("environments")[app.node.try_get_context("env")]
env = Environment(account=conf["account"], region=conf["region"])

stack = UserStack(
    app, '-'.join([conf["name"], "user", "stack"]), conf, env=env
)

app.synth()