from aws_cdk import (core as cdk, aws_ecs as ecs, aws_ecr as ecr, aws_ec2 as ec2, aws_iam as iam)

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core


class CdkStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        ecr_repository = ecr.Repository(self,
                "ecs-devops-sandbox-repository",
                repository_name="ecs-devops-sandbox-repository")

        vpc = ec2.Vpc(self,
                "ecs-devops-sandbox-vpc",
                max_azs=3)

        cluster = ecs.Cluster(self,
                "ecs-devops-sandbox-cluster",
                cluster_name="ecs-devops-sandbox-cluster",
                vpc=vpc)

        execution_role = iam.Role(self,
                "ecs-devops-sandbox-execution-role",
                assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
                role_name="ecs-devops-sandbox-execution-role")
        execution_role.add_to_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            resources=["*"],
            actions=[
                'ecr:GetAuthorizationToken',
                'ecr:BatchCheckLayerAvailability',
                'ecr:GetDownloadUrlForLayer',
                'ecr:BatchGetImage',
                'logs:CreateLogStream',
                'logs:PutLogEvents'
                ]
            ))

        task_definition = ecs.FargateTaskDefinition(self,
            "ecs-devops-sandbox-task-definition",
            execution_role=execution_role,
            family="ecs-devops-sandbox-task-definition")

        container = task_definition.add_container(
            "ecs-devops-sandbox",
            image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample"))

        service = ecs.FargateService(self,
            "ecs-devops-sandbox-service",
            cluster=cluster,
            task_definition=task_definition,
            service_name="ecs-devops-sandbox-service")
