from helpers import server, client, socket, file, menu, network
from services import message_service
import main_menu
import threading
from services import data_service as data_svc
from multiprocessing import Process, Manager
from globals import variables

CLIENTS = {}
HOST = "localhost"
PORT = int(file.env("SOCKET_PORT", 8050))

if __name__ == '__main__':
    # Restaura as mensagens e contatos anteriores
    data_svc.restore_data()

    # Sincroniza os dados com outros parceiros
    print("Sincronizando dados, por favor, aguarde...")
    data_svc.sync_data()

    server_thread = threading.Thread(target=server.start)
    server_thread.start()
    
    network_thread = threading.Thread(target=network.check_network)
    network_thread.daemon = True  # Define a thread como um daemon para que ela termine quando o programa principal terminar
    network_thread.start()

    # Permite que subthreads iniciem:
    file.delete_file('stop.z', True)

    main_menu.show()
    # Permite que subthreads parem:
    server.stop()