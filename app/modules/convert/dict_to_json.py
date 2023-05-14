import json

def dict_to_json(dict) -> str:
    '''Returns a dictionary in JSON format'''
    return json.dumps(dict, indent=4)