from helpers import server, client, socket, file, menu, network
from services import message_service
import main_menu
import threading
from services import data_service as data_svc
from multiprocessing import Process, Manager
from globals import variables
import sys

CLIENTS = {}
HOST = "localhost"
PORT = int(file.env("SOCKET_PORT", 8050))

if __name__ == '__main__':
    if (len(sys.argv) < 3):
        exit("\nQuantidade de argumentos inválidos! O mínimo requerido são 2 (main.py {user} {command} {optional:content}) conforme o exemplo: main.py Marcos read-messages")
    
    # Restaura as mensagens e contatos anteriores
    data_svc.restore_data()

    # Sincroniza os dados com outros parceiros
    data_svc.sync_data()

    server_thread = threading.Thread(target=server.start)
    server_thread.start()
    
    network_thread = threading.Thread(target=network.check_network)
    network_thread.daemon = True  # Define a thread como um daemon para que ela termine quando o programa principal terminar
    network_thread.start()

    # Permite que subthreads iniciem:
    file.delete_file('stop.z', True)

    manager = Manager()
    variables.INTERPROC_MESSAGES = manager.Queue()
    messages_terminal = Process(target=message_service.render_messages, args=(variables.INTERPROC_MESSAGES,))
    messages_terminal.start()

    if data_svc.check_username(sys.argv[1]):
        data_svc.set_username(sys.argv[1])
        content = None
        if (len(sys.argv) > 3):
            content = sys.argv[3]
        main_menu.run(sys.argv[2], content)
    else:
        print("ERROR: Nome de usuário informado não corresponde ao usuário conectado! Se deseja usar outro username, primeiro faça LOGOFF da conta atualmente conectada.")
    
    # Permite que subthreads parem:
    server.stop()