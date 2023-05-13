import json
import uuid

class File:
    def json_to_dict(self, path: str) -> any:
        '''Returns a JSON file as a dictionary'''
        with open(path, 'r') as file:
            content = file.readlines()
            dict = json.loads(''.join(content))
            return dict

    def dict_to_json(self, dict) -> str:
        '''Returns a dictionary in JSON format'''
        return json.dumps(dict, indent=4)

    def dict_to_text(self, dict):
        '''Returns a dictionary as a multiline string'''
        array = []
        for ingredient in dict:
            array.append('{} {}'.format(dict[ingredient], ingredient))
        return '\n'.join(array)

class Crypto():
    def generate_id(self):
        '''Generate a unique ID using the uuid module.'''
        return str(uuid.uuid4().hex)[:6]
