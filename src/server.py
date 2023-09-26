import socket
import threading
from helpers import client_helper
from helpers import file
import os

def main():
    global server_socket
    try:
        while not os.path.exists("stop.z"):
            print(". ")
            client_socket, client_address = server_socket.accept()
            print(f"Conexão estabelecida com {client_address}")
            client_handler = threading.Thread(target=client_helper.handle_request, args=(client_socket,))
            client_handler.start()
    except KeyboardInterrupt:
        print("Servidor interrompido pelo usuário.")
    finally:
        server_socket.close
        print("Servidor encerrado")

if __name__ == '__main__':
    HOST = "localhost"
    PORT = int(file.env("SOCKET_PORT", 8050))
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(HOST, PORT)
    server_socket.listen(35)
    main()
