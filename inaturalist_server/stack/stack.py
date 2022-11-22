from aws_cdk import (
    aws_ec2 as ec2,
    Stack
)

from constructs import Construct

class ServerStack(Stack):
    def __init__(self, scope: Construct, id: str, conf: dict, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        vpc = ec2.Vpc.from_lookup(
            self, '-'.join([conf['name'], 'vpc']),
            is_default=True
        )

        instance_type = ec2.InstanceType(conf['instance_type'])

        # https://cloud-images.ubuntu.com/locator/ec2/
        machine_image = ec2.MachineImage.generic_linux({
            'us-east-1': 'ami-072d6c9fae3253f26' # ubuntu 20.04 amd64 
        })

        security_group_name = '-'.join([conf['name'], 'security', 'group'])
        security_group = ec2.SecurityGroup(
            self, security_group_name, security_group_name=security_group_name,
            allow_all_outbound=True, vpc=vpc
        )
        security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(22),
            'allow ssh from anywhere'
        )
        security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(80),
            'allow http from anywhere'
        )
        security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(443),
            'allow https from anywhere'
        )
        security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(3000),
            'allow inat app from anywhere'
        )
        security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(4000),
            'allow inat api from anywhere'
        )
        security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(5432),
            'allow postgres access from anywhere'
        )

        server_name = conf['name']
        server = ec2.Instance(
            self, server_name, instance_name=server_name,
            vpc=vpc, instance_type=instance_type,
            machine_image=machine_image,
            block_devices=[
                ec2.BlockDevice(
                    device_name="/dev/sda1",
                    volume=ec2.BlockDeviceVolume.ebs(conf['volume'])
                )
            ],
            key_name=server_name, # note you'll need to create the keypair 
            security_group=security_group
        )