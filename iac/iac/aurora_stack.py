from aws_cdk import (
    Stack,
    aws_rds,
    aws_ec2,
)
from constructs import Construct

class AuroraStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Use default VPC
        default_vpc = aws_ec2.Vpc.from_lookup(self, "DefaultVpc", is_default=True)
        
        # Create security group for Aurora in default VPC
        aurora_security_group = aws_ec2.SecurityGroup(
            self, "AuroraSecurityGroup",
            vpc=default_vpc,
            description="Security group for Aurora Serverless V2 cluster",
            allow_all_outbound=False
        )

        aurora_security_group.add_ingress_rule(
            peer=aws_ec2.Peer.ipv4(default_vpc.vpc_cidr_block),
            connection=aws_ec2.Port.tcp(5432),
            description="Allow PostgreSQL access from default VPC"
        )

        self.aurora_serverless_v2 = aws_rds.DatabaseCluster(self, "VectorDataBase",
                                                            engine=aws_rds.DatabaseClusterEngine.aurora_postgres(
                                                                version=aws_rds.AuroraPostgresEngineVersion.VER_16_3),
                                                            serverless_v2_min_capacity=0,
                                                            serverless_v2_max_capacity=2,
                                                            SecondsUntilAutoPause=900,
                                                            writer=aws_rds.ClusterInstance.serverless_v2("writer"),
                                                            vpc=default_vpc,
                                                            vpc_subnets=aws_ec2.SubnetSelection(
                                                                subnet_type=aws_ec2.SubnetType.PUBLIC),
                                                            enable_data_api=True,
                                                            credentials=aws_rds.Credentials.from_generated_secret(
                                                                'postgres'),
                                                            security_groups=[aurora_security_group]
                                                            )

        self.cluster_arn = self.aurora_serverless_v2.cluster_arn
        self.secret_arn = self.aurora_serverless_v2.secret.secret_arn

