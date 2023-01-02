from constructs import Construct
from aws_cdk import (
    Stage
)
from apigateway.infrastructure.apigateway_stack import PlayerDomainGatewayStack
from lambda_function.infratructure.player_ingest_stage import PlayerIngestStack


class PlayerDomainStage(Stage):

    def __init__(self, scope: Construct, id: str, rest_api_id, root_resource_id, **kwargs):
        super().__init__(scope, id, **kwargs)

        handler = PlayerIngestStack(self)

        rest_api = PlayerDomainGatewayStack(self, 
            rest_api_id=rest_api_id, 
            root_resource_id=root_resource_id,
            handler_arn=handler.function_arn)

        rest_api.root.add_method("ANY")

        return rest_api
