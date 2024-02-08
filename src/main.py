from helpers import server, client, socket, file, menu
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
    data_svc.sync_data()

    server_service = threading.Thread(target=server.start)
    server_service.start()

    # Permite que subthreads iniciem:
    file.delete_file('stop.z', True)

    manager = Manager()
    variables.INTERPROC_MESSAGES = manager.Queue()
    messages_terminal = Process(target=message_service.render_messages, args=(variables.INTERPROC_MESSAGES,))
    messages_terminal.start()

    main_menu.show()
    # Permite que subthreads parem:
    server.stop()