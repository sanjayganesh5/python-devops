import json
from time import sleep
from utility import get_property, custom_response, CustomLogger, get_application_token, release_application_token

APP_ENV = get_property('APP_ENV')
IS_LOCAL = 'local' == APP_ENV
log_group = f'/aws/lambda/job/{APP_ENV}-jobFunctionOne'


def main(**kwargs):
    token = None
    logger = CustomLogger(log_group)
    query_params = kwargs['query_params']
    body = kwargs['body']
    logger.info(f'query_params: {query_params}, body: {body}')
    # start your code here
    try:
        token = get_application_token()
        logger.info('sleeping for 20 seconds')
        sleep(20)
        logger.info('woke up after 20 seconds')
    except Exception as e:
        logger.error(e)
    finally:
        release_application_token(token)
    # end your code here
    return custom_response(
        status_code=200,
        content_type='application/json',
        body=json.dumps(
            {
                'message': 'job_one',
                'query_params': query_params,
                'body': body
            }
        )
    )
