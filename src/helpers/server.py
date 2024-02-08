import socket
import time
from helpers import socket as CustomSocket, file, client
from globals.variables import GROUPS, PRIVATE_KEY
from controllers import partner_controller, message_controller
import json

LOG_FILE_NAME = 'server.log'
HOST = client.get_local_ip()
PORT = int(file.env("SOCKET_PORT", 8050))
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(35)

def handle_request(client_socket, client_ip):
    message = None
    try:
        message = CustomSocket.receive_json_message(client_socket)
        file.log(LOG_FILE_NAME, "Mensagem recebida: ")
        file.log(LOG_FILE_NAME, json.dumps(message))
        if message:
            code = message.get("code")
            if code == "Zx01":
                partner_controller.share_partner(message)
            elif code == "Zx02":
                partner_controller.remove_partner(message)
            elif code == "Zx11":
                message_controller.intercept_messages(message)
        else:
            file.log(LOG_FILE_NAME, client_ip + " enviou uma mensagem vazia")
    except Exception as e:
        file.log(LOG_FILE_NAME, f"Algum erro aconteceu: {e}")
        file.log(LOG_FILE_NAME, f"Conteúdo da msg: {str(message)}")
    finally:
        client_socket.close()
    return message
        
def start():
    global server_socket
    try:
        file.log(LOG_FILE_NAME, f"Servidor iniciado. Aguardando conexões em {HOST}:{PORT}...")
        while not file.file_exists('stop.z'):
            file.log(LOG_FILE_NAME, "Aguardando conexões...")
            client_socket, client_address = server_socket.accept()
            file.log(LOG_FILE_NAME, f"Conexão estabelecida com {client_address}")
            # client_handler = threading.Thread(target=handle_request, args=(client_socket,client_address[0],))
            # client_handler.start()
            handle_request(client_socket, client_address[0])
    except KeyboardInterrupt:
        file.log(LOG_FILE_NAME, "Servidor interrompido pelo usuário.")
    finally:
        server_socket.close()
        file.log(LOG_FILE_NAME, "Servidor encerrado")

def stop():
    file.create_file('stop.z', '', True)
    file.log(LOG_FILE_NAME, "Parando servidor...")
    time.sleep(1)  # Aguarda um curto período antes de tentar reiniciar
    loopback_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    loopback_socket.connect((HOST, PORT))
    loopback_socket.close()
    time.sleep(1)
    disconnect_server()
    file.log(LOG_FILE_NAME, "Servidor parado.")

def disconnect_server():
    server_socket.close()
    file.log(LOG_FILE_NAME, "Servidor desconectado.")