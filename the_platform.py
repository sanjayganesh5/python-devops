import importlib
from urllib import parse
from utility import get_property, get_cloudwatch_logger

TEXT_CONTENT_TYPE = 'text/plain'


def handler_response(**kwargs):
    return {
        'statusCode': kwargs['status_code'],
        'headers': {
            'Content-Type': kwargs['content_type'],
        },
        'body': kwargs['body']
    }


def function_handler(url_path, event):
    function_name = url_path[url_path.rindex('/') + 1:]
    try:
        if 'queue' in url_path:
            api_function = getattr(importlib.import_module('queue'), function_name)
        elif 'job' in url_path:
            api_function = getattr(importlib.import_module('job'), function_name)
        elif 'custom-command' in url_path:
            api_function = getattr(importlib.import_module('custom_command'), function_name)
        else:
            raise ModuleNotFoundError(f'{function_name} not found')
    except ModuleNotFoundError:
        return handler_response(status_code=404, content_type=TEXT_CONTENT_TYPE, body=f'{function_name} not found')
    else:
        return api_function.main(event)


def api_handler(resource, function_name, event):
    query_params = event['queryParameters']
    body = event['body']
    print(f'function_name: {function_name}, query_params: {query_params}, body: {body}')
    try:
        if resource == 'queue':
            api_function = getattr(importlib.import_module('queue'), function_name)
        elif resource == 'job':
            api_function = getattr(importlib.import_module('job'), function_name)
        elif resource == 'custom-command':
            api_function = getattr(importlib.import_module('custom_command'), function_name)
        else:
            raise ModuleNotFoundError(f'{resource} not found')
    except ModuleNotFoundError:
        return handler_response(status_code=404, content_type=TEXT_CONTENT_TYPE, body=f'{resource} not found')
    else:
        return api_function.main(query_params, body)


def handler(event, context):
    print('event: ', event)
    if 'httpMethod' in event:
        path_params = event['pathParameters']
        resource = path_params['resource']
        if resource in ('queue', 'job', 'custom-command'):
            print('package: ', resource)
            function_name = parse.unquote(path_params['functionName'])
            return api_handler(resource, function_name.replace('-', '_'), event)
        else:
            return handler_response(status_code=404, content_type=TEXT_CONTENT_TYPE, body=f'{resource} not found')
    else:
        url_path = event['rawPath']
        print('url_path: ', url_path)
        if url_path:
            return function_handler(url_path, event)
        else:
            return handler_response(status_code=404, content_type=TEXT_CONTENT_TYPE, body=f'{url_path} not found')