
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


class PlayerDomainGatewayStack(Stack):

    def __init__(self, scope, *, rest_api_id, rootResourceId, handler_arn) -> None:
        super().__init__(scope, id, **kwargs)

        api = RestApi.from_rest_api_attributes(self,
            rest_api_id=rest_api_id,
            root_resource_id=root_resource_id
        )

        lambda_handler = _lambda.from_function_arn(handler_arn)

        lambda_integration = apigateway.LambdaIntegration(handler)

        player = api.root.add_resource("player", default_integration=lambda_integration)
        player.add_method("GET") # GET /player
        player.add_method("POST") # POST /player

        player_id = player.add_resource("{player_id}")
        player_id.add_method("PATCH") # PATCH /player/{player_id}
        player_id.add_method("DELETE") # DELETE /player/{player_id}