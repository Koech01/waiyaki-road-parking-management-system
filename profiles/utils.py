import uuid

def get_uuid():
    user_uuid = str(uuid.uuid4())[:8].replace('-', '').lower()
    return user_uuid
