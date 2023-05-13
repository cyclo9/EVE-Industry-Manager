import uuid

def generate_id():
    '''Generate a unique ID using the UUID module.'''
    return str(uuid.uuid4().hex[:6])