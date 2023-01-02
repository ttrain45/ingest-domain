import json
import datetime
import boto3

from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.typing import LambdaContext

client = boto3.client('events')

logger = Logger(service="PlayerInjestLambda")
tracer = Tracer(service="PlayerInjestLambda")


@logger.inject_lambda_context
@tracer.capture_lambda_handler
def handler(event: dict, context: LambdaContext) -> str:

    logger.info(event)

    ingest_event = [
        {
            'Source': 'InjestLambda',
            'DetailType': event['path'].split('/')[1].upper(),
            'Detail': json.dumps(event),
            'EventBusName': 'CoreEventBus'
        },
    ]

    logger.info({'ingest_event': ingest_event})

    core_eventbridge_response = client.put_events(
        Entries=ingest_event
    )

    logger.info('Core Bridge kicked off from Ingest Lambda')
