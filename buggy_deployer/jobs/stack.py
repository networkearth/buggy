from aws_cdk import (
    aws_ecr as ecr,
    aws_batch as batch,
    Stack
)

from constructs import Construct

def prefix(conf):
    return '-'.join([conf['namespace'], conf['stage']])

class BatchJobStack(Stack):
    def __init__(self, scope: Construct, id: str, conf: dict, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        repository_name = '-'.join([prefix(conf), conf['job_name']])
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
            image=f"{conf['account']}.dkr.ecr.{conf['region']}.amazonaws.com/{prefix(conf)}-{conf['job_name']}:latest",
            resource_requirements=[vcpu_property, memory_property],
            execution_role_arn=f"arn:aws:iam::{conf['account']}:role/{conf['execution_role']}",
            job_role_arn=f"arn:aws:iam::{conf['account']}:role/{conf['execution_role']}",
            fargate_platform_configuration=batch.CfnJobDefinition.FargatePlatformConfigurationProperty(
                platform_version="1.4.0"
            )
        )

        batch_job_name = '-'.join([prefix(conf), conf['job_name']])
        batch_job = batch.CfnJobDefinition(
            self, batch_job_name,
            job_definition_name=batch_job_name,
            type='container',
            container_properties=container_properties,
            platform_capabilities=["FARGATE"]
        )
