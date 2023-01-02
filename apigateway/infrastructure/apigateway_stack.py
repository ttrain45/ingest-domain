
from constructs import Construct
from aws_cdk import (
    Stack,
    aws_events_targets as target,
    aws_lambda as _lambda,
    aws_logs as logs,
    Duration,
    aws_iam as iam,
    aws_apigateway as apigateway,
    CfnOutput,
    aws_events as events,
    aws_lambda_python_alpha as python
)
import json
import os


class ApigatewayStack(Stack):

    def __init__(self, scope, id: str, handler_arn, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        rest_api_log_group = logs.LogGroup(self, "IngestLogs")

        rest_api = apigateway.RestApi(
            self,
            "IngestGateway",
            cloud_watch_role=True,
            deploy_options=apigateway.StageOptions(
                access_log_destination=apigateway.LogGroupLogDestination(rest_api_log_group),
                access_log_format=apigateway.AccessLogFormat.clf()
            )
        )

        handler = python.PythonFunction.from_function_arn(self, "IngestLambdaHandler", handler_arn)

        rest_api.root.add_proxy(
            any_method=True,
            default_integration=apigateway.LambdaIntegration(handler)
        )

        
                                


        