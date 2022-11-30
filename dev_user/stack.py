from aws_cdk import (
    aws_s3 as s3,
    aws_iam as iam,
    aws_secretsmanager as secrets,
    Stack
)

from constructs import Construct

class UserStack(Stack):
    def __init__(self, scope: Construct, id: str, conf: dict, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        user_name = conf['name']
        user = iam.User(
            self, user_name, user_name=user_name
        )

        group = iam.Group(
            self, user_name + "s", group_name=user_name + "s"
        )

        user.add_to_group(group)

        bucket_name = 'buggy-job-bucket'
        bucket = s3.Bucket.from_bucket_name(
            self, bucket_name, bucket_name=bucket_name
        )
        bucket.grant_read_write(group)

        bucket_name = 'buggy-backup-bucket'
        bucket = s3.Bucket.from_bucket_name(
            self, bucket_name, bucket_name=bucket_name
        )
        bucket.grant_read_write(group)

        group.add_to_policy(
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

        secret_name = '-'.join(['buggy-dev', 'inaturalist'])
        secret = secrets.Secret.from_secret_name_v2(
            self, secret_name, secret_name=secret_name
        )
        secret.grant_read(group)

        secret_name = '-'.join(['buggy-dev', 'secret-key'])
        secret = secrets.Secret.from_secret_name_v2(
            self, secret_name, secret_name=secret_name
        )
        secret.grant_read(group)

        secret_name = '-'.join(['buggy-dev', 'kobo'])
        secret = secrets.Secret.from_secret_name_v2(
            self, secret_name, secret_name=secret_name
        )
        secret.grant_read(group)