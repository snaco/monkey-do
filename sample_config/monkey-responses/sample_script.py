'''Sample script with the boilerplate to interact with monkey-do'''
# pylint: disable=used-before-assignment,invalid-name,undefined-variable
#inputs
query_params: dict = globals()['query_params']
route: str = globals()['route']
body: str = globals()['body']

#outputs
globals()['response'] = 'Hello there.'
globals()['status'] = 200
