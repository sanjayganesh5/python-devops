import json
from utility import get_cloudwatch_logger, get_property

APP_ENV = get_property('APP_ENV')
IS_LOCAL = 'local' == APP_ENV
logger = get_cloudwatch_logger(
    name=__name__,
    log_group=f'/aws/lambda/queue/{APP_ENV}-queueFunctionOne',
    is_local=IS_LOCAL
)


def main(**kwargs):
    query_params = kwargs['query_params']
    body = kwargs['body']
    logger.info(f'query_params: {query_params}, body: {body}')
    return {
        'statusCode': 200,
        'body': json.dumps(
            {
                'message': 'function_one',
                'query_params': query_params,
                'body': body
            }
        )
    }
