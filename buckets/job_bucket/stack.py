from aws_cdk import (
    aws_s3 as s3,
    Stack
)

from constructs import Construct

class BucketStack(Stack):
    def __init__(self, scope: Construct, id: str, conf: dict, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        bucket_name = '-'.join([conf['stage'], conf['name']])
        bucket = s3.Bucket(
            self, bucket_name, bucket_name=bucket_name,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            encryption=s3.BucketEncryption.S3_MANAGED,
            enforce_ssl=True,
        )