import json
from models.partner import Partner
from helpers import client, file
from globals.variables import MY_IP
import traceback
import time
from globals.methods import get_last_answer_host, set_last_answer_host

DEFAULT_TIMEOUT = 4

def send_message(client_socket, message: str):
    client_socket.send(message.encode('utf-8') if isinstance(message, str) else message)

def receive_json_message(data) -> dict[str, any]:
    if not data:
        return None
    try:
        return json.loads(data.decode('utf-8'))
    except Exception as e:
        raise e

def send_message_to_partner(partner: Partner, message, is_json = True):
    timeout = DEFAULT_TIMEOUT
    successful = False
    
    try:
        try:
            partner.socket = client.connect_to_server(partner.host, partner.port)
        except Exception as e:
            raise e
        
        if is_json:
            send_message(partner.socket, json.dumps(message))
        else:
            send_message(partner.socket, message)
        
        while timeout > 0:
            time.sleep(1)
            file.log("socket.log", f"partner-host: {partner.host}, answer-host: {get_last_answer_host}")
            if get_last_answer_host() == partner.host:
                successful = True
                break
            timeout -= 1
        
        client.disconnect_client(partner.socket)
        set_last_answer_host(None)
        partner.socket = None
        
        return successful
    except Exception as e:
        file.log('error.log', traceback.format_exc())
        set_last_answer_host(None)
        return False
    
def send_message_to_online_partner(destiny: Partner, message, is_json = True, stop_if_me = True):
    # Busca o próximo parceiro online no anel:
    while destiny.is_offline and destiny.next_partner is not None:
        destiny = destiny.next_partner
    
    if stop_if_me and destiny.host == MY_IP:
        return True
    
    # Tenta enviar mensagem para o próximo parceiro online no anel:
    file.log("info.log", "send_message_to_online_partner para parceiro " + destiny.host)
    successful = send_message_to_partner(destiny, message, is_json)
    while not successful and (destiny.next_partner is not None):
        # destiny.is_offline = True
        destiny = destiny.next_partner
        if stop_if_me and destiny.host == MY_IP:
            return True
        successful = send_message_to_partner(destiny, message, is_json)
        file.log("info.log", "send_message_to_online_partner para parceiro " + destiny.host)
    return successful