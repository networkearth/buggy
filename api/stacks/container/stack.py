"""
Container Stack
"""

from aws_cdk import (
    aws_ecr as ecr,
    Stack
)

from constructs import Construct

class ContainerStack(Stack):
    """
    Container Stack
    """

    # pylint: disable=redefined-builtin,invalid-name
    def __init__(self, scope: Construct, id: str, conf: dict, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        repository_name = '-'.join([conf['stage'], conf['name']])
        ecr.Repository(
            self, repository_name, repository_name=repository_name
        )
