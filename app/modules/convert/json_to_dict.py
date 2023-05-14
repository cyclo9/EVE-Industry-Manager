import json

def json_to_dict(path: str) -> any:
    '''Returns a JSON file as a dictionary'''
    with open(path, 'r') as file:
        content = file.readlines()
        dict = json.loads(''.join(content))
        return dict