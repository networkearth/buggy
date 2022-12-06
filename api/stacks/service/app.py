from aws_cdk import App, Environment

from stack import ServiceStack

app = App()

stage = "-".join([app.node.try_get_context("namespace"), app.node.try_get_context("environment")])
conf = app.node.try_get_context("environments")[stage]
env = Environment(account=conf["account"], region=conf["region"])
conf['stage'] = stage

stack = ServiceStack(
    app, '-'.join([stage, conf["name"], "service", "stack"]), conf, env=env
)

app.synth()