import json
from models.partner import Partner
from helpers import client, file
from globals.variables import MY_IP
import traceback

def send_message(client_socket, message: str):
    client_socket.send(message.encode('utf-8') if isinstance(message, str) else message)

def receive_json_message(client_socket) -> dict[str, any]:
    data = client_socket.recv(8192)
    if not data:
        return None
    try:
        return json.loads(data.decode('utf-8'))
    except Exception as e:
        raise e
        print(f"Erro na decodificação JSON: {e}")
        return None

def send_message_to_partner(partner: Partner, message, is_json = True):
    # if partner.socket:
    #     client.disconnect_client(partner.socket)
    try:
        try:
            if partner.socket is None:
                partner.socket = client.connect_to_server(partner.host, partner.port)
        except Exception as e:
            raise e
        if is_json:
            send_message(partner.socket, json.dumps(message))
        else:
            send_message(partner.socket, message)
        client.disconnect_client(partner.socket)
        partner.socket = None
        return True
    except Exception as e:
        file.log('error.log', traceback.format_exc())
        return False
    
def send_message_to_online_partner(destiny: Partner, message, is_json = True, stop_if_me = True):
    # Busca o próximo parceiro online no anel:
    while destiny.is_offline and destiny.next_partner is not None:
        destiny = destiny.next_partner
    
    if stop_if_me and destiny.host == MY_IP:
        return True
    
    # Tenta enviar mensagem para o próximo parceiro online no anel:
    successful = send_message_to_partner(destiny, message, is_json)
    while not successful and (destiny.next_partner is not None):
        # destiny.is_offline = True
        destiny = destiny.next_partner
        if stop_if_me and destiny.host == MY_IP:
            return True
        successful = send_message_to_partner(destiny, message, is_json)
    return successful