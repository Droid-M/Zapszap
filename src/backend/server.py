import socket
import threading
from helpers import socket
from helpers import file
import os

HOST = "localhost"
PORT = int(file.env("SOCKET_PORT", 8050))
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(35)

def start(on_waiting_new_connection, on_new_client_connected, on_server_interrupted):
    global server_socket
    try:
        while not os.path.exists("stop.z"):
            on_waiting_new_connection()
            client_socket, client_address = server_socket.accept()
            on_new_client_connected(client_socket, client_address)
            client_handler = threading.Thread(target=socket.handle_request, args=(client_socket,))
            client_handler.start()
    except KeyboardInterrupt:
        on_server_interrupted()
    finally:
        server_socket.close()
        print("Servidor encerrado")