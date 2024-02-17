from helpers import file, client

_private_key = None
_last_answer_host = {}

def get_private_key():
    global _private_key
    if _private_key is None:
        _private_key = client.serialize_key(file.read_backup_file("private_key.zap"), True)
    return _private_key

def get_last_answer_host(timestamp: str):
    return _last_answer_host.get(timestamp)

def set_last_answer_host(host: str, timestamp: str):
    file.log("answer.log", f"Nova resposta de host: {host} | time: {timestamp}")
    global _last_answer_host
    _last_answer_host[timestamp] = host
    
def remove_last_answer_host(timestamp: str):
    global _last_answer_host
    host = _last_answer_host.pop(timestamp, None)
    file.log("answer.log", f"Removendo host: {host} | time: {timestamp}")
    return host