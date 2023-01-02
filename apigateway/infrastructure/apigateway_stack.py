
from constructs import Construct
from aws_cdk import (
    Stack,
    aws_events_targets as target,
    aws_lambda as _lambda,
    Duration,
    aws_iam as iam,
    aws_apigateway as apigateway,
    CfnOutput,
    aws_events as events,
    aws_lambda_python_alpha as python
)
import json
import os
from apigateway.infrastructure.player_domain_gateway_stack import IngestDomainGatewayStack
from lambda_function.infratructure.player_ingest_stack import PlayerIngestStack


class ApigatewayStack(Stack):

    def __init__(self, scope, id: str, handler_arn, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        rest_api = apigateway.RestApi(self, "IngestGateway")

        rest_api.root.add_proxy(
            any_method=True,
            default_integration=python.PythonFunction.from_function_arn(self, "IngestLambdaHandler", handler_arn)
        )

        PlayerIngestStack(self, "PlayerIngestStack")

        IngestLambdaHandler = python.PythonFunction.from_function_name(
            self, "IngestLambdaHandler", "IngestLambdaHandler")

        player_domain = IngestDomainGatewayStack(
            self,
            "IngestDomainGatewayStack",
            rest_api_id=rest_api.rest_api_id,
            root_resource_id=rest_api.rest_api_root_resource_id,
            handler_arn=IngestLambdaHandler.function_arn
        )




        
                                


        