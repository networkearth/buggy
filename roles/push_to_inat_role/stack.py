from aws_cdk import (
    aws_s3 as s3,
    aws_iam as iam,
    Stack
)

from constructs import Construct

class RoleStack(Stack):
    def __init__(self, scope: Construct, id: str, conf: dict, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        role_name = conf['name']
        role = iam.Role(
            self, role_name, role_name=role_name,
            assumed_by=iam.ServicePrincipal('ecs-tasks.amazonaws.com')
        )

        bucket_name = 'buggy-job-bucket'
        bucket = s3.Bucket.from_bucket_name(
            self, bucket_name, bucket_name=bucket_name
        )
        bucket.grant_read_write(role)

        bucket_name = 'buggy-backup-bucket'
        bucket = s3.Bucket.from_bucket_name(
            self, bucket_name, bucket_name=bucket_name
        )
        bucket.grant_read_write(role)

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