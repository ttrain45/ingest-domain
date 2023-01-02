
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


class ApigatewayStack(Stack):

    def __init__(self, scope, *, handler_arn) -> None:
        super().__init__(scope, id, **kwargs)

        api = apigateway.RestApi(self, "myapi",
            proxy=False
        )




        
                                


        