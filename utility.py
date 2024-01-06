import inspect
import os
import uuid
import boto3
import jproperties
from datetime import datetime

PROP_FILE = f'{os.path.dirname(os.path.abspath(__file__))}/application.properties'
APP_ENV = os.environ['APP_ENV']
TEXT_CONTENT_TYPE = 'text/plain'


def get_property(key: str) -> str:
    if APP_ENV == 'local':
        configs = jproperties.Properties()
        with open(PROP_FILE, 'rb') as config_file:
            configs.load(config_file)
        return configs.get(key).data
    else:
        return os.environ[key]


def custom_response(**kwargs):
    """
    Requires the following kwargs: status_code, content_type, body.
    Convert the response text based on the content type before passing it as the value for the body in kwargs.
    For example,
    If the content type is application/json, then convert the body to json using json.dumps() method.
    @param kwargs:
    @return:
    """
    return {
        'statusCode': kwargs['status_code'],
        'headers': {
            'Content-Type': kwargs['content_type'],
        },
        'body': kwargs['body']
    }


class CustomLogger:
    def __init__(self, log_group):
        self.service_up = True
        self.client = boto3.client('logs')
        self.log_group = log_group
        self.log_stream = f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%f")}/[$Latest]{str(uuid.uuid4())}'
        try:
            response = self.client.create_log_stream(logGroupName=log_group, logStreamName=self.log_stream)
            print(f'Created log stream {self.log_stream} in log group {log_group}. Response: {response}')
        except self.client.exceptions.ResourceAlreadyExistsException:
            print(f'Log stream {self.log_stream} already exists. Writing logs to it.')
        except self.client.exceptions.ServiceUnavailableException:
            self.service_up = False
            print(f'Service unavailable. Writing to default log stream.')  # write logs to default log stream

    # define a private method to write to cloudwatch
    def __write_to_cloudwatch(self, message):
        if self.service_up:
            self.client.put_log_events(
                logGroupName=self.log_group,
                logStreamName=self.log_stream,
                logEvents=[
                    {
                        'timestamp': int(datetime.now().timestamp() * 1000),
                        'message': message
                    }
                ]
            )
        else:
            print(message)

    def info(self, message):
        function_name = inspect.currentframe().f_back.f_code.co_name  # get the name of the calling function
        formatted_message = f'{function_name} | INFO | {message}'
        self.__write_to_cloudwatch(formatted_message)

    def error(self, message):
        function_name = inspect.currentframe().f_back.f_code.co_name  # get the name of the calling function
        formatted_message = f'{function_name} | ERROR | {message}'
        self.__write_to_cloudwatch(formatted_message)

    def warning(self, message):
        function_name = inspect.currentframe().f_back.f_code.co_name  # get the name of the calling function
        formatted_message = f'{function_name} | WARNING | {message}'
        self.__write_to_cloudwatch(formatted_message)
