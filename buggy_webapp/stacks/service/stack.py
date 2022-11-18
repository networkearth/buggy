from aws_cdk import (
    aws_ecs as ecs,
    aws_ec2 as ec2,
    aws_ecr as ecr,
    aws_ecs_patterns as patterns,
    Stack
)

from constructs import Construct

class ServiceStack(Stack):
    def __init__(self, scope: Construct, id: str, conf: dict, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        service_name = '-'.join([conf['name'], 'service'])
        patterns.ApplicationLoadBalancedFargateService(
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
                container_port=5001
            ),
            load_balancer_name=service_name,
            assign_public_ip=True
        )