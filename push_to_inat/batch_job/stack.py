from aws_cdk import (
    aws_ecr as ecr,
    aws_batch as batch,
    Stack
)

# https://stackoverflow.com/questions/72645571/aws-batch-timeout-connecting-to-ecr

from constructs import Construct

class BatchJobStack(Stack):
    def __init__(self, scope: Construct, id: str, conf: dict, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        repository_name = '-'.join([conf['stage'], conf['name']])
        repository = ecr.CfnRepository(
            self, repository_name + '-ecr',
            repository_name=repository_name
        )

        vcpu_property = batch.CfnJobDefinition.ResourceRequirementProperty(
            type='VCPU',
            value=conf['vcpu']
        )

        memory_property = batch.CfnJobDefinition.ResourceRequirementProperty(
            type='MEMORY',
            value=conf['memory']
        )

        container_properties = batch.CfnJobDefinition.ContainerPropertiesProperty(
            image=f"{conf['account']}.dkr.ecr.{conf['region']}.amazonaws.com/{conf['stage']}-{conf['name']}:latest",
            resource_requirements=[vcpu_property, memory_property],
            execution_role_arn=f"arn:aws:iam::{conf['account']}:role/{conf['stage']}-{conf['name']}",
            job_role_arn=f"arn:aws:iam::{conf['account']}:role/{conf['stage']}-{conf['name']}",
            fargate_platform_configuration=batch.CfnJobDefinition.FargatePlatformConfigurationProperty(
                platform_version="1.4.0"
            ),
            network_configuration=batch.CfnJobDefinition.NetworkConfigurationProperty(
                assign_public_ip="ENABLED"
            )
        )

        batch_job_name = '-'.join([conf['stage'], conf['name']])
        batch_job = batch.CfnJobDefinition(
            self, batch_job_name,
            job_definition_name=batch_job_name,
            type='container',
            container_properties=container_properties,
            platform_capabilities=["FARGATE"]
        )
