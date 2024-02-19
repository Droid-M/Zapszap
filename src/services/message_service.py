from multiprocessing import Process, Manager
from DAOs import messageDAO, partnerDAO
from globals import variables
from helpers import file, network, menu, socket, key
from services import data_service
import keyboard
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
    old_messages = None
    last_key_state = False  # Estado da tecla "T" na última iteração do loop
    show_again = False
    while not keyboard.is_pressed('esc'):
        if show_again or old_messages != messageDAO.to_json():
            menu.clear_console()
            print("\nExibindo mensagens... Pressione ESC para voltar ou Delete para escrever uma mensagem\n")
            for msg in variables.MESSAGES:
                print(msg.__str__())
            old_messages = messageDAO.to_json()
            show_again = False
    
        key_state = keyboard.is_pressed("delete")
        if key_state and not last_key_state:
            send_group_message()
            show_again = True
        last_key_state = key_state
    clear_keyboard_buffer()
    menu.clear_console()

def send_group_message():
    if not network.is_online():
        print("\nVerifique se você está conectado(a) à internet e tente novamente!\n")
        time.sleep(5)
        return
    me = partnerDAO.get_me()
    destiny = partnerDAO.get_my_next_partner()
    
    if destiny:
        clear_keyboard_buffer()
        msg = input("\n\nInforme a mensagem que você deseja enviar: \n")
        
        # Remove a letra "t" do início da mensagem, se presente
        if msg.startswith("t"):
            msg = msg[1:]
        
        messageDAO.register(MY_IP, msg, me.name)
        print("Enviando mensagem...")
        messages = key.encrypt_message(messageDAO.to_json(), destiny.public_key)
        if not socket.send_message_to_online_partner(destiny, {'code': 'Zx11', 'merge_messages': 1, "from": MY_IP, 'messages_list': messages, "sender": me.name}):
            print("\nFalha ao enviar mensagem! Aparentemente, nenhum parceiro está online no momento ou a sua conexão caiu. Tente mais tarde.\n\n")
            time.sleep(5)
    else:
        print("\nVocê não faz parte de nenhum grupo! Para enviar mensagens, é necessário se conectar com alguém.\n")
        time.sleep(5)
    data_service.backup_data()