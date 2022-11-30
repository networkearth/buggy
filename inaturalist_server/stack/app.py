from aws_cdk import App, Environment

from stack import ServerStack

app = App(context={"env": "dev"})

conf = app.node.try_get_context("environments")[app.node.try_get_context("env")]
env = Environment(account=conf["account"], region=conf["region"])

stack = ServerStack(
    app, '-'.join([conf["name"], "server", "stack"]), conf, env=env
)

app.synth()