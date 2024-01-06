import json
from time import sleep
from utility import get_property, CustomLogger

APP_ENV = get_property('APP_ENV')
IS_LOCAL = 'local' == APP_ENV
log_group = f'/aws/lambda/queue/{APP_ENV}-queueFunctionOne'


def main(**kwargs):
    # logging handler
    logger = CustomLogger(log_group)
    query_params = kwargs['query_params']
    body = kwargs['body']
    logger.info(f'query_params: {query_params}, body: {body}')
    # start your code here
    logger.info('sleeping for 10 seconds')
    sleep(10)
    logger.info('woke up after 10 seconds')
    # end your code here
    return {
        'statusCode': 200,
        'body': json.dumps(
            {
                'message': 'queue_one',
                'query_params': query_params,
                'body': body
            }
        )
    }
