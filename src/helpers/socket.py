import json
from models.partner import Partner
from helpers import client, file
from globals.variables import MY_IP
import traceback
import time
from globals.methods import get_last_answer_host, set_last_answer_host, remove_last_answer_host
from DAOs import partnerDAO

DEFAULT_TIMEOUT = 4

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
    timestamp = str(time.time_ns())
    
    try:
        try:
            partner.socket = client.connect_to_server(partner.host, partner.port)
        except Exception as e:
            raise e
        
        if is_json:
            message["TS"] = timestamp
            message = json.dumps(message)
        
        file.log("info.log", f"{partner.host}:{partner.port}. {'port é do tipo inteiro' if isinstance(partner.port, int) else 'port não é do tipo inteiro'}")
        partner.socket.sendto(message.encode('utf-8') if isinstance(message, str) else message, (partner.host, partner.port))
        
        while timeout > 0:
            time.sleep(DEFAULT_TIMEOUT / 5)
            if get_last_answer_host(timestamp) == partner.host:
                successful = True
                break
            timeout -= 1
        file.log("socket.log", f"partner-host: {partner.host}, answer-host: {get_last_answer_host(timestamp)}")
        
        client.disconnect_client(partner.socket)
        partner.socket = None
        
        return successful
    except Exception as e:
        file.log('error.log', traceback.format_exc())
        return False
    finally:
        remove_last_answer_host(timestamp)

def send_message_to_guest(host: str, port: int, message, is_json = True):
    timeout = DEFAULT_TIMEOUT
    successful = False
    socket = None
    timestamp = str(time.time_ns())
    
    try:
        try:
            socket = client.connect_to_server(host, port)
        except Exception as e:
            raise e
        
        if is_json:
            message = json.dumps(message)
            message["TS"] = timestamp
            
        socket.sendto(message.encode('utf-8') if isinstance(message, str) else message, (host, port))
        
        while timeout > 0:
            time.sleep(DEFAULT_TIMEOUT / 5)
            file.log("socket.log", f"guest-host: {host}")
            if get_last_answer_host(timestamp) == host:
                successful = True
                break
            timeout -= 1
        
        client.disconnect_client(socket)
        socket = None
        
        return successful
    except Exception as e:
        file.log('error.log', traceback.format_exc())
        return False
    finally:
        remove_last_answer_host(timestamp)
    
def send_message_to_online_partner(destiny: Partner, message, is_json = True, stop_if_me = True):
    # Busca o próximo parceiro online no anel:
    while destiny.is_offline:
        destiny = destiny.next_partner
        if destiny is None:
            destiny = partnerDAO.get_first()
    
    if stop_if_me and destiny.host == MY_IP:
        return True
    
    # Tenta enviar mensagem para o próximo parceiro online no anel:
    successful = send_message_to_partner(destiny, message, is_json)
    while destiny.is_offline or not successful:
        file.log("info.log", "send_message_to_online_partner - Falha ao enviar msg para parceiro " + destiny.host)
        # destiny.is_offline = True
        destiny = destiny.next_partner
        if stop_if_me and destiny.host == MY_IP:
            return True
        successful = send_message_to_partner(destiny, message, is_json)
    if successful:
        file.log("info.log", "send_message_to_online_partner - Êxito ao enviar msg para parceiro " + destiny.host)
    return successful