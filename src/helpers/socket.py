import socket
import json
from models.partner import Partner
from helpers import client, key, file
from helpers import type as typeHelper
import base64

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
        print(f"Erro ao enviar mensagem para {partner.socket}. Erro: {e}. Por favor, verifique sua conexão e tente novamente.")
        return False