
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
from apigateway.infrastructure.player_domain_gateway_stack import PlayerDomainGatewayStack
from lambda_function.infratructure.player_ingest_stack import PlayerIngestStack


class ApigatewayStack(Stack):

    def __init__(self, scope, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        rest_api = apigateway.RestApi(self, "IngestGateway")

        rest_api.root.add_method("ANY")

        PlayerIngestStack(self, "PlayerIngestStack")

        playerIngestLambdaHandler = python.PythonFunction.from_function_name(
            self, "PlayerIngestLambdaHandler", "PlayerIngestLambdaHandler")

        player_domain = PlayerDomainGatewayStack(
            self,
            "PlayerDomainGatewayStack",
            rest_api_id=rest_api.rest_api_id,
            root_resource_id=rest_api.rest_api_root_resource_id,
            handler_arn=playerIngestLambdaHandler.function_arn
        )




        
                                


        