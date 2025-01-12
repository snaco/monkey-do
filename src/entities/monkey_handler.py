"""Entity for the route configurations"""
from entities.monkey_response import MonkeyResponse
from entities.exceptions import MonkeySeeConfigException


class MonkeyHandler():
    """Object containing the response, method, and route for an endpoint"""
    handler_id: str
    method: str
    route: str
    response: MonkeyResponse

    def __init__(self, handler_id: str, method: str, route: str, response: dict):
        self.handler_id = handler_id
        self.method = method
        self.route = route
        if 'body_file' in response.keys():
            with open(f'config/{response["body_file"]}', encoding='utf-8') as file:
                mnk_response =  {
                    'status': response['status'],
                    'body': file.read()
                }
                if 'mime_type' in response.keys():
                    mnk_response.update({'mime_type': response['mime_type']})
                self.response = MonkeyResponse(**mnk_response)
        elif 'body' in response.keys() or 'script' in response.keys():
            self.response = MonkeyResponse(**response)
        else:
            raise MonkeySeeConfigException(f'Monkey see error! The {method} {route} endpoint has no body, body_file, or script.')

    def get_response(self, query_params: dict[str,str] = None):
        '''Executes the script if one exists, otherwise will return the monkey response'''
        code_prefix = open('src/templates/script_prefix.py', encoding='UTF-8').read()
        code_suffix = open('src/templates/script_suffix.py', encoding='UTF-8').read()
        if self.response.script:
            globals()['query_params'] = query_params
            globals()['response'] = None
            globals()['route'] = self.route
            #TODO : Implement body parsing       pylint:disable=fixme
            globals()['body'] = None
            file_contents = open(f'config/{self.response.script}', encoding='UTF-8').read()
            code = f'{code_prefix}{file_contents}{code_suffix}'
            exec(code, globals()) # pylint: disable=exec-used
            return MonkeyResponse(status=self.response.status, body=globals()['response'], mime_type=self.response.mime_type)
        return self.response
