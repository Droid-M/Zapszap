from multiprocessing import Process, Manager
from DAOs import messageDAO, partnerDAO
from globals import variables
from helpers import file, input as InputHelper, menu, socket, key
from services.partner_service import forward_message_to_active_member
from services import data_service
import keyboard
import json
import time
from globals.variables import MY_IP
import sys

def render_messages(shared_messages):
    while not file.file_exists('stop.z'):
        if not shared_messages.empty():
            message: variables.Message = shared_messages.get()
            print(str(message))
        
def clear_keyboard_buffer():
    # while keyboard.is_pressed(''):
    #     keyboard.read_event()
    time.sleep(0.5)
    sys.stdin.flush()

def see_chat():
    old_messages = None
    last_key_state = False  # Estado da tecla "T" na última iteração do loop
    while not keyboard.is_pressed('esc'): 
        if old_messages != messageDAO.to_json():
            menu.clear_console()
            print("\nExibindo mensagens... Pressione ESC para voltar ou T para escrever uma mensagem\n")
            for msg in variables.MESSAGES:
                print(msg.__str__())
            old_messages = messageDAO.to_json()
    
        key_state = keyboard.is_pressed("t")
        if key_state and not last_key_state:
            clear_keyboard_buffer()
            send_group_message()
            print("\nExibindo mensagens... Pressione ESC para voltar ou T para escrever uma mensagem\n")
        last_key_state = key_state
    clear_keyboard_buffer()

def send_group_message():
    destiny = partnerDAO.get_me().next_partner
    if destiny is None and not partnerDAO.empty():
        destiny = partnerDAO.get_first()
        while (destiny is not None) and destiny.host == MY_IP:
            destiny = destiny.next_partner
    if destiny:
        msg = input("\n\nInforme a mensagem que você deseja enviar: \n")
        messages = key.encrypt_message(json.dumps(messageDAO.to_list_of_dicts()), destiny.public_key)
        msg = key.encrypt_message(msg, destiny.public_key)
        print("Enviando mensagem...")
        if not socket.send_message_to_online_partner(destiny, {'code': 'Zx11', "from": MY_IP, 'new_message': msg, 'messages_list': messages, "sender": partnerDAO.get_me().name}):
            print("\nFalha ao enviar mensagem! Aparentemente, nenhum parceiro está online no momento. Tente mais tarde.\n\n")
    else:
        print("\nVocê não faz parte de nenhum grupo! Para enviar mensagens, é necessário se conectar com alguém.\n")
    data_service.backup_data()