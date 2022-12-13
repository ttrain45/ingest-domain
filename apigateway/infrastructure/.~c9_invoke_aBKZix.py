
from constructs import Construct
from aws_cdk import (
    Stack,
    aws_events_targets as target,
    aws_lambda as _lambda,
    Duration,
    aws_iam as iam,
    aws_apigatewayv2 as apigatewayv2,
    aws_apigatewayv2_alpha as apigatewayv2_alpha,
    aws_apigatewayv2_integrations_alpha as http_lambda_integration,
    CfnOutput,
    aws_events as events,
    aws_lambda_python_alpha as python
)
import os


class ApigatewayStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        ### Create HttpApi Role ###
        api_role = iam.Role(self,
                            'CoreEventBusIntegrationRole',
                            assumed_by=iam.ServicePrincipal(
                                "apigateway.amazonaws.com"),
                            description="API Gateway Role used for integration with CoreEventBus and other resources")

        ### Retrieve Core Event Bus from event bus name ###
        core_event_bus = events.EventBus.from_event_bus_name(
            self, "CoreEventBus", "CoreEventBus")

        # You now have to manage the Role policies yourself as there are no
        # L2 functions for EventBridge to APIGateway
        api_role.add_to_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            resources=[core_event_bus.event_bus_arn],
            actions=['events:PutEvents']))

        api_role.add_to_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            resources=['*'],
            actions=['lambda:InvokeFunction']))

        ### Create HttpApi ###
        http_api = apigatewayv2_alpha.HttpApi(self,
                                              'CoreEventBustIngestHttpApi')

        ### Create ApiGateway Integration ###
        http_api_cfn_integration = apigatewayv2.CfnIntegration(self,
                                                               "CoreEventBusHttpApiIntegration",
                                                               api_id=http_api.api_id,
                                                               integration_type="AWS_PROXY",
                                                               integration_subtype="EventBridge-PutEvents",
                                                               credentials_arn=api_role.role_arn,
                                                               request_parameters={
                                                                   "Source": "ingest-api",
                                                                   "DetailType": "team",
                                                                   "Detail": "$request.body",
                                                                   "EventTime": "$context.requestTimeEpoch",
                                                                   "EventBusName": core_event_bus.event_bus_arn
                                                               },
                                                               payload_format_version="1.0",
                                                               timeout_in_millis=10000
                                                               )

        http_api_cfn_route = apigatewayv2.CfnRoute(self,
                                                   "CoreEventBusHttpApiRoute",
                                                   api_id=http_api.api_id,
                                                   route_key="POST /api/teams",
                                                   target="integrations/{}".format(
                                                       http_api_cfn_integration.ref)
                                                   )

        ### Create ApiGateway Integration Need to work on naming here once it works ###
        http_api_cfn_integration_player = apigatewayv2.CfnIntegration(self,
                                                                      "CoreEventBusHttpApiIntegrationPlayer",
                                                                      api_id=http_api.api_id,
                                                                      integration_type="AWS_PROXY",
                                                                      integration_subtype="EventBridge-PutEvents",
                                                                      credentials_arn=api_role.role_arn,
                                                                      request_parameters={
                                                                          "Source": "ingest-api",
                                                                          "DetailType": "player",
                                                                          "Detail": "$request.body",
                                                                          "EventTime": "$context.requestTimeEpoch",
                                                                          # Plan to add timestamp as key / value pair passed in
                                                                          "EventBusName": core_event_bus.event_bus_arn
                                                                      },
                                                                      payload_format_version="1.0",
                                                                      timeout_in_millis=10000
                                                                      )

        http_api_cfn_route_player = apigatewayv2.CfnRoute(self,
                                                          "CoreEventBusHttpApiRoutePlayer",
                                                          api_id=http_api.api_id,
                                                          route_key="POST /api/player",
                                                          target="integrations/{}".format(
                                                              http_api_cfn_integration_player.ref)
                                                          )

        read_player_lambda = python.PythonFunction.from_function_name(
            self, "ReadPlayer", "ReadPlayer")

        ### Create ApiGateway Integration Need to work on naming here once it works ###
        http_api_cfn_integration_read_player = apigatewayv2.CfnIntegration(self,
                                                                           "ReadPlayerLambdaHttpApiIntegrationPlayer",
                                                                           api_id=http_api.api_id,
                                                                           integration_type="AWS_PROXY",
                                                                           integration_uri="https://cingfcrkcinp23w2cosldl4mmq0qekdt.lambda-url.us-east-1.on.aws/",
                                                                           credentials_arn=api_role.role_arn,
                                                                           payload_format_version="1.0",
                                                                           timeout_in_millis=10000
                                                                           )

        http_api_cfn_route_read_player = apigatewayv2.CfnRoute(self,
                                                               "ReadPlayerLambdaHttpApiRoutePlayer",
                                                               api_id=http_api.api_id,
                                                               route_key="GET /api/player",
                                                               target="integrations/{}".format(
                                                                   http_api_cfn_integration_read_player.ref)
                                                               )
