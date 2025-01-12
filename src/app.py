"""Main executor for monkey-do"""
from click import command
from flask import Flask, request, render_template_string
from flask.wrappers import Response
import yaml

from entities import MonkeyResponse, MonkeySeeConfig
from utilities import routes_match


app = Flask('monkey_do_server')
all_methods = [
    'GET',
    'POST',
    'PUT',
    'HEAD',
    'DELETE',
    'CONNECT',
    'OPTIONS',
    'TRACE',
    'PATCH'
]


@app.route('/', methods=all_methods)
def monkey_root() -> Response:
    """handler for the root route"""
    response = generate_response('', request.method)
    if response.mime_type == 'text/html':
        return render_template_string(response.body)
    return Response(response.body, status=response.status, mimetype=response.mime_type)


@app.route('/<path:path>', methods=all_methods)
def mock_point(path: str) -> Response:
    """The proxy endpoint"""
    query_params = None
    if request.args:
        query_params = request.args.to_dict()
    response = generate_response(path, request.method, query_params)
    if response.mime_type == 'text/html':
        return render_template_string(response.body)
    return Response(response.body, status=response.status, mimetype=response.mime_type)


def generate_response(route: str, method: str, query_params: dict[str, str] = None) -> MonkeyResponse:
    """Generate a MonkeyResponse from the mnkc"""
    handler_matches = list(filter(lambda handler: routes_match(handler.route, route), load_config().handlers))
    for handler in handler_matches:
        if handler.method == method:
            return handler.get_response(query_params)
    return MonkeyResponse(404, f'Monkey see no {method} defined for {route}, monkey do 404.')


def load_config() -> MonkeySeeConfig:
    """loads the config file into a MonkeySeeConfig object"""
    with open('config/config.mnkc', encoding='utf-8') as file:
        mnkc_yaml = yaml.safe_load(file.read())
        return MonkeySeeConfig(**mnkc_yaml)


@command()
def start_server():
    """Start the flask server"""
    app.run(debug=True, port=load_config().port)


if __name__ == '__main__':
    start_server()
