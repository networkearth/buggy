from aws_cdk import (
    aws_ecs as ecs,
    aws_ecr as ecr,
    aws_elasticloadbalancingv2 as elbv2,
    aws_ecs_patterns as patterns,
    aws_iam as iam,
    aws_route53 as route53,
    Stack
)

from constructs import Construct

class ServiceStack(Stack):
    def __init__(self, scope: Construct, id: str, conf: dict, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        namespace, environment = conf['stage'].split('-')
        domain_name = f'{namespace}.{environment}.{conf["name"]}.networkearth.io'
        hosted_zone = route53.PublicHostedZone(
            self, '-'.join([conf['stage'], conf['name'], 'hosted-zone']),
            zone_name=domain_name
        )

        service_name = '-'.join([conf['stage'], conf['name']])
        service = patterns.ApplicationLoadBalancedFargateService(
            self, service_name,
            memory_limit_mib=512, cpu=256, desired_count=1,
            task_image_options=patterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_ecr_repository(
                    repository=ecr.Repository.from_repository_name(
                        self, '-'.join([conf['stage'], conf['name'], 'repository']),
                        repository_name='-'.join([conf['stage'], conf['name']])
                    ),
                    tag='latest',
                ),
                container_port=5002,
                task_role=iam.Role.from_role_name(
                    self, '-'.join([conf['stage'], conf['name'], 'role']),
                    role_name='-'.join([conf['stage'], conf['name']])
                )
            ),
            load_balancer_name=service_name,
            assign_public_ip=True,
            domain_name=domain_name,
            domain_zone=hosted_zone,
            #protocol=elbv2.ApplicationProtocol.HTTPS
        )
