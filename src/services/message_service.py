from multiprocessing import Process, Manager
from DAOs import messageDAO, partnerDAO
from globals import variables
from helpers import file, network, menu, socket, key, input as InputHelper
from services import data_service
import time
from globals.variables import MY_IP
import sys

def render_messages(shared_messages):
    while not file.file_exists('stop.z'):
        if not shared_messages.empty():
            message: variables.Message = shared_messages.get()
            print(str(message))
        
def clear_keyboard_buffer():
    sys.stdin.flush()

def see_chat():
    for msg in variables.MESSAGES:
        print(msg.__str__())

def send_group_message(msg):
    # if not network.is_online():
    #     print("ERROR: Você está offline")
    #     return
    
    me = partnerDAO.get_me()
    destiny = partnerDAO.get_my_next_partner()
    
    if destiny:
        messageDAO.register(MY_IP, msg, me.name)
        messages = key.encrypt_message(messageDAO.to_json(), destiny.public_key)
        if not socket.send_message_to_online_partner(destiny, {'code': 'Zx11', 'merge_messages': 1, "from": MY_IP, 'messages_list': messages, "sender": me.name}):
            print("ERROR: Falha ao enviar mensagem! Verifique sua conexão e se seus parceiros estão disponíveis no momento.")
        else:
            print("INFO: Mensagem enviada!")
    else:
        print("ERROR: Você não está conectado(a) a nenhum grupo!")
    data_service.backup_data()