from constructs import Construct
from aws_cdk import (
    Stage
)
from apigateway.infrastructure.apigateway_stack import ApigatewayStack


class ApigatewayStage(Stage):

    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        rest_api = ApigatewayStack(self, 'Apigateway')

        rest_api.root.add_method("ANY")

        return rest_api
