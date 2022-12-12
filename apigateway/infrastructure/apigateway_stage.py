from constructs import Construct
from aws_cdk import (
    Stage
)
from apigateway.infrastructure.apigateway_stack import ApigatewayStack


class ApigatewayStage(Stage):

    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        service = ApigatewayStack(self, 'Apigateway')
