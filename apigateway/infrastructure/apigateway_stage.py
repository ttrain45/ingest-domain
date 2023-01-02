from constructs import Construct
from aws_cdk import (
    Stage
)
from apigateway.infrastructure.apigateway_stack import ApigatewayStack
from lambda_function.infratructure.gateway_ingest_stack import GatewayIngestStack


class ApigatewayStage(Stage):

    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        gateway_ingest_stack = GatewayIngestStack(self, "GatewayIngestStack")

        ApigatewayStack(self, 'IngestApiGateway', gateway_ingest_stack.handler_function_arn)