from aws_cdk import (
    aws_s3 as s3,
    aws_iam as iam,
    aws_secretsmanager as secrets,
    Stack
)

from constructs import Construct

class RoleStack(Stack):
    def __init__(self, scope: Construct, id: str, conf: dict, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        role_name = '-'.join([conf['stage'], conf['name']])
        role = iam.Role(
            self, role_name, role_name=role_name,
            assumed_by=iam.ServicePrincipal('ecs-tasks.amazonaws.com')
        )

        bucket_name = '-'.join([conf['stage'], 'job'])
        bucket = s3.Bucket.from_bucket_name(
            self, bucket_name, bucket_name=bucket_name
        )
        bucket.grant_read_write(role)

        secret_name = '-'.join([conf['stage'], 'inaturalist'])
        secret = secrets.Secret.from_secret_name_v2(
            self, secret_name, secret_name=secret_name
        )
        secret.grant_read(role)

        role.add_to_policy(
            iam.PolicyStatement(
                principals=[],
                actions=[
                    "ecr:*",
                    "logs:*"
                ],
                resources=[
                    '*'
                ]
            )
        )

        role.add_to_policy(
            iam.PolicyStatement(
                principals=[],
                actions=[
                    "batch:SubmitJob"
                ],
                resources=[
                    '*'
                ]
            )
        )