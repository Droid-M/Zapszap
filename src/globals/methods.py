from helpers import file, client

_private_key = None
_last_answer_host = None

def get_private_key():
    global _private_key
    if _private_key is None:
        _private_key = client.serialize_key(file.read_backup_file("private_key.zap"), True)
    return _private_key

def get_last_answer_host():
    return _last_answer_host

def set_last_answer_host(host: str):
    global _last_answer_host
    _last_answer_host = host