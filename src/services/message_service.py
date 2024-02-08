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
    sys.stdin.flush()

def see_chat():
    # message = variables.Message(MY_IP, '1234', 'mensagem de teste')
    # variables.INTERPROC_MESSAGES.put(message)
    # print("Mensagem visualizada")
    old_messages = None
    # while input("insira Y para continuar no loop: ").lower() == 'y':
    press_lock = False
    while not keyboard.is_pressed('esc'): 
        if old_messages != messageDAO.to_json():
            menu.clear_console()
            print("Exibindo mensagens... Pressione ESC para voltar ou T para escrever uma mensagem")
            for msg in variables.MESSAGES:
                print(msg.__str__())
            old_messages = messageDAO.to_json()
        if keyboard.is_pressed("t") and not press_lock:
            press_lock = True
            clear_keyboard_buffer()
            send_group_message()
        time.sleep(0.1)
        press_lock = False
        clear_keyboard_buffer()

    # while InputHelper.non_blocking_getch() != "esc":
        # if len(old_messages) != len(variables.MESSAGES):
        #     print(str(messageDAO.get_last_message()))
        #     old_messages = variables.MESSAGES

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
        result = socket.send_message_to_partner(destiny, {'code': 'Zx11', "from": MY_IP, 'new_message': msg, 'messages_list': messages})
    else:
        print("\nVocê não faz parte de nenhum grupo! Para enviar mensagens, é necessário se conectar com alguém.\n")
    data_service.backup_data()