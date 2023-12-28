import json
from utility import get_cloudwatch_logger, get_property, CloudWatchHandler

APP_ENV = get_property('APP_ENV')
IS_LOCAL = 'local' == APP_ENV
log_group = f'/aws/lambda/queue/{APP_ENV}-jobFunctionOne'


def main(**kwargs):
    # logging handler
    custom_handler = CloudWatchHandler(log_group=log_group)
    logger = get_cloudwatch_logger(is_local=IS_LOCAL, name=__name__, custom_handler=custom_handler)
    query_params = kwargs['query_params']
    body = kwargs['body']
    logger.info(f'query_params: {query_params}, body: {body}')
    # start your code here
    # ...
    # end your code here
    logger.removeHandler(custom_handler)
    return {
        'statusCode': 200,
        'body': json.dumps(
            {
                'message': 'job_one',
                'query_params': query_params,
                'body': body
            }
        )
    }
