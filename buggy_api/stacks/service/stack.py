from sys import intern
from aws_cdk import (
    aws_ecs as ecs,
    aws_elasticloadbalancingv2_targets as targets,
    aws_elasticloadbalancingv2 as elb,
    aws_ec2 as ec2,
    aws_ecr as ecr,
    aws_ecs_patterns as patterns,
    Stack
)

from constructs import Construct

class ServiceStack(Stack):
    def __init__(self, scope: Construct, id: str, conf: dict, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        vpc = ec2.Vpc.from_lookup(
            self, '-'.join([conf['name'], 'vpc']),
            is_default=True
        )

        service_name = '-'.join([conf['name'], 'service'])
        service = patterns.ApplicationLoadBalancedFargateService(
            self, service_name,
            memory_limit_mib=512, cpu=256, desired_count=1,
            task_image_options=patterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_ecr_repository(
                    repository=ecr.Repository.from_repository_name(
                        self, '-'.join([conf['name'], 'repository']),
                        repository_name=conf['name']
                    ),
                    tag='latest',
                ),
                container_port=5002
            ),
            load_balancer_name=service_name,
            assign_public_ip=True,
            vpc=vpc
        )

        # in order to have a static ip we need to put this
        # behind a network load balancer

        nlb_name = '-'.join([conf['name'], 'network-load-balancer'])
        nlb = elb.NetworkLoadBalancer(
            self, nlb_name, load_balancer_name=nlb_name,
            vpc=vpc, internet_facing=True, cross_zone_enabled=True
        )

        listener = nlb.add_listener('http-listener', port=80)

        target = targets.AlbTarget(service.load_balancer, 80)
        listener.add_targets('http-target', targets=[target], port=80)
