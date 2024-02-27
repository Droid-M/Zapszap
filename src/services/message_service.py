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
    choice = None
    while choice != 's':
        menu.clear_console()
        choice = input("Insira:\n\tS - Sair\n\tE - Escrever mensagem\n\tL - Ler mensagens\nSua escolha: ").lower()
        if choice == 's':
            break
        elif choice == 'l':
            if len(variables.MESSAGES):
                print("\nExibindo mensagens...\n")
                for msg in variables.MESSAGES:
                    print(msg.__str__())
            else:
                print("\nNão há mensagens disponíveis!\n")
            input("\nPressione Enter para prosseguir...\n")
    
        elif choice == 'e':
            send_group_message()
    menu.clear_console()

def send_group_message():
    # if not network.is_online():
    #     print("\nVerifique se você está conectado(a) à internet e tente novamente!\n")
    #     time.sleep(5)
    #     return
    
    me = partnerDAO.get_me()
    destiny = partnerDAO.get_my_next_partner()
    
    if destiny:
        clear_keyboard_buffer()
        msg = input("\n\nInforme a mensagem que você deseja enviar: \n")
        
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