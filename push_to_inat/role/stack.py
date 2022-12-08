"""
Role Stack
"""

from aws_cdk import (
    aws_s3 as s3,
    aws_iam as iam,
    Stack
)

from constructs import Construct

class RoleStack(Stack):
    """
    Role Stack
    """
    # pylint: disable=invalid-name,redefined-builtin
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

        bucket_name = '-'.join([conf['stage'], 'backup'])
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
