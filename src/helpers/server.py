import socket
import time
from helpers import socket as CustomSocket, file, client
from controllers import partner_controller, message_controller
import json
import traceback
from globals import methods
from DAOs import partnerDAO

LOG_FILE_NAME = 'server.log'
HOST = client.get_local_ip()
PORT = int(file.env("SOCKET_PORT", 8050))
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

def handle_request(message, client_address):
    client_ip = client_address[0]
    try:
        message = CustomSocket.receive_json_message(message)
        file.log(LOG_FILE_NAME, f"Mensagem recebida de {client_ip}: ")
        file.log(LOG_FILE_NAME, json.dumps(message))
        if message:
            code = message.get("code") 
            if code == "Zx20":
                methods.set_last_answer_host(client_ip, message.get("TS"))
            else:
                replies_client(client_ip, message.pop("TS", None), True)
                if code == "Zx01":
                    partner_controller.share_partner(message)
                elif code == "Zx02":
                    partner_controller.remove_partner(message)
                elif code == "Zx11":
                    message_controller.intercept_messages(message)
        else:
            file.log(LOG_FILE_NAME, client_ip + " enviou uma mensagem vazia")
    except Exception as e:
        file.log("error.log", traceback.format_exc())
        
def replies_client(client_ip: str, timestamp: str, successful: bool):
    file.log(LOG_FILE_NAME, f"Respondendo à {client_ip}:")
    file.log(LOG_FILE_NAME, json.dumps({"code": "Zx20", "TS": timestamp, "success": successful}))
    CustomSocket.send_response_message(client_ip, PORT, {"code": "Zx20", "success": successful}, timestamp)

def start():
    try:
        file.log(LOG_FILE_NAME, f"Servidor iniciado. Aguardando mensagens em {HOST}:{PORT}...")
        while not file.file_exists('stop.z'):
            file.log(LOG_FILE_NAME, "Aguardando mensagens...")
            message, client_address = server_socket.recvfrom(8192)  # Tamanho máximo do datagrama é 8192 bytes
            handle_request(message, client_address)
    except KeyboardInterrupt:
        file.log(LOG_FILE_NAME, "Servidor interrompido pelo usuário.")
    finally:
        server_socket.close()
        file.log(LOG_FILE_NAME, "Servidor encerrado")

def stop():
     # Verifica se o socket está pronto para uso
    if server_socket:
        file.create_file('stop.z', '', False)
        file.log(LOG_FILE_NAME, "Parando servidor...")
        time.sleep(0.3)
        try:
            server_socket.sendto(b"", (HOST, PORT))  # Envia um datagrama vazio para desbloquear o recvfrom
        except OSError as e:
            print(f"ERROR: Erro ao enviar dados: {e}")
        time.sleep(0.3)
        disconnect_server()
        file.log(LOG_FILE_NAME, "Servidor parado.")
    else:
        print("ERROR: Socket não inicializado corretamente.")

def disconnect_server():
    server_socket.close()
    file.log(LOG_FILE_NAME, "Servidor desconectado.")
