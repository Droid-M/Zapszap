from helpers import file, client
import json

_private_key = None
ANSWERS_BACKUP_FILE = "answers.zap"

def get_private_key():
    global _private_key
    if _private_key is None:
        _private_key = client.serialize_key(file.read_backup_file("private_key.zap"), True)
    return _private_key

def get_last_answers():
    _last_answer_host = file.read_backup_file(ANSWERS_BACKUP_FILE)
    file.log("answer.log", "Respondedores atuais:")
    file.log("answer.log", json.dumps(_last_answer_host))
    return _last_answer_host if _last_answer_host is not None else {}

def get_last_answer_host(timestamp):
    _last_answer_host = get_last_answers()
    return _last_answer_host.get(timestamp)

def set_last_answer_host(host, timestamp):
    file.log("answer.log", f"Nova resposta de host: {host} | time: {timestamp}")
    _last_answer_host = get_last_answers()
    _last_answer_host[timestamp] = host
    file.write_backup_file(ANSWERS_BACKUP_FILE, json.dumps(_last_answer_host))
    
def remove_last_answer_host(timestamp):
    file.log("answer.log", f"Tentando remover time: {timestamp}")
    _last_answer_host = get_last_answers()
    # host = _last_answer_host.pop(timestamp, None)
    # file.log("answer.log", f"Removeu host: {host} | time: {timestamp}")
    # file.write_backup_file(ANSWERS_BACKUP_FILE, json.dumps(_last_answer_host))
    # return host