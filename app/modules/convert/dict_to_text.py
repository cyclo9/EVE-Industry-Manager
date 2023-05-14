import json

def dict_to_text(dict):
    '''Returns a dictionary as a multiline string'''
    array = []
    for ingredient in dict:
        array.append('{} {}'.format(dict[ingredient], ingredient))
    return '\n'.join(array)