import importlib
from urllib import parse
from utility import custom_response, TEXT_CONTENT_TYPE


def function_handler(url_path, event):
    print(f'url_path: {url_path}, event: {event}')
    function_name = url_path[url_path.rindex('/') + 1:]
    print(f'function_name: {function_name}')
    function_name = function_name.replace('-', '_')
    try:
        if 'queue' in url_path:
            api_function = importlib.import_module(f'queues.{function_name}')
        elif 'job' in url_path:
            api_function = importlib.import_module(f'jobs.{function_name}')
        elif 'custom-command' in url_path:
            api_function = importlib.import_module(f'custom_commands.{function_name}')
        else:
            raise ModuleNotFoundError(f'{function_name} not found')
    except ModuleNotFoundError:
        return custom_response(status_code=404, content_type=TEXT_CONTENT_TYPE, body=f'{url_path} not found')
    else:
        body = event.get('body', {})
        query_params = event['queryStringParameters']
        return api_function.main(query_params=query_params, body=body)


def api_handler(resource, function_name, event):
    print(f'function_name: {function_name}, event: {event}')
    try:
        if resource == 'queue':
            api_function = importlib.import_module(f'queues.{function_name}')
        elif resource == 'job':
            api_function = importlib.import_module(f'jobs.{function_name}')
        elif resource == 'custom-command':
            api_function = importlib.import_module(f'custom_commands.{function_name}')
        else:
            raise ModuleNotFoundError(f'{resource} not found')
    except ModuleNotFoundError:
        return custom_response(status_code=404, content_type=TEXT_CONTENT_TYPE,
                               body=f'{resource}.{function_name} not found')
    else:
        body = event['body']
        query_params = event['queryStringParameters']
        return api_function.main(query_params=query_params, body=body)


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
            return custom_response(status_code=404, content_type=TEXT_CONTENT_TYPE, body=f'{resource} not found')
    else:
        url_path = event['rawPath']
        print('url_path: ', url_path)
        if url_path:
            return function_handler(url_path, event)
        else:
            return custom_response(status_code=404, content_type=TEXT_CONTENT_TYPE, body='rawPath not found in event')
