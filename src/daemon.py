from helpers import server, file, network
import threading
from services import data_service as data_svc
from multiprocessing import Process, Manager
import sys

CLIENTS = {}
HOST = "localhost"
PORT = int(file.env("SOCKET_PORT", 8050))

if __name__ == '__main__':
    # Restaura as mensagens e contatos anteriores
    data_svc.restore_data()

    # Sincroniza os dados com outros parceiros
    data_svc.sync_data()

    network_thread = threading.Thread(target=network.check_network)
    network_thread.daemon = True  # Define a thread como um daemon para que ela termine quando o programa principal terminar
    network_thread.start()

    # Permite que o servidor seja iniciado em loop:
    file.delete_file('stop.z', True)

    server.start()