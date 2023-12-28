import logging
import os
import uuid
import boto3
import jproperties
from datetime import datetime

PROP_FILE = f'{os.path.dirname(os.path.abspath(__file__))}/application.properties'
APP_ENV = os.environ['APP_ENV']


def get_property(key: str) -> str:
    if APP_ENV == 'local':
        configs = jproperties.Properties()
        with open(PROP_FILE, 'rb') as config_file:
            configs.load(config_file)
        return configs.get(key).data
    else:
        return os.environ[key]


class CloudWatchHandler(logging.Handler):
    def __init__(self, log_group, log_stream):
        logging.Handler.__init__(self)
        self.client = boto3.client('logs')
        self.log_group = log_group
        self.log_stream = log_stream
        self.formatter = logging.Formatter('%(funcName)s - %(levelname)s - %(message)s')

    def emit(self, record):
        try:
            response = self.client.create_log_stream(logGroupName=self.log_group, logStreamName=self.log_stream)
            print(f'Created log stream {self.log_stream} in log group {self.log_group}. Response: {response}')
        except self.client.exceptions.ResourceAlreadyExistsException:
            print(f'Log stream {self.log_stream} already exists. Writing logs to it.')
        self.client.put_log_events(
            logGroupName=self.log_group,
            logStreamName=self.log_stream,
            logEvents=[
                {
                    'timestamp': int(record.created * 1000),
                    'message': self.format(record)
                }
            ]
        )


def get_cloudwatch_logger(is_local=False, **kwargs):
    if is_local:
        formatter = logging.Formatter('%(funcName)s - %(levelname)s - %(message)s')
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger = logging.getLogger(kwargs['name'])
        logger.setLevel(logging.INFO)
        logger.addHandler(stream_handler)
        return logger
    log_group = kwargs.get('log_group')
    log_stream = f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}/[$Latest]{str(uuid.uuid4())}'
    logger = logging.getLogger(kwargs['name'])
    logger.setLevel(logging.INFO)
    logger.addHandler(CloudWatchHandler(log_group, log_stream))
    return logger
