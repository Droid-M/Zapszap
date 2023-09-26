import socket
# import ast
from helpers import file

# Configurações do cliente
HOST = file.env("RASPBERRY_IP")  #IP da Raspberry PI
PORT = int(file.env("RASPBERRY_SOCKET_PORT"))  # Porta para comunicação

def receive_data():
    """Informa as etiquetas lidas pelo servidor
    Returns:
        Retorna None caso nenhuma etiqueta tenha sido informada pelo servidor ou houver falha na comunicação. Ou retorna True caso o servidor
        tenha enviado ao menos uma etiqueta
    """
    # Inicializa o cliente
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    data_received = None
    print("Conexão estabelecida com a Raspberry Pi")
    data_to_send = "READ_SENSORS"
    try:
        sent_bytes = client_socket.send(data_to_send.encode())
        if sent_bytes == len(data_to_send):
            # Recebe dados da Raspberry Pi
            data_received = client_socket.recv(1024).decode()
            data_received = data_received.split(',') if data_received else None
    except Exception as e:
        print(e)
    finally:
        # Encerra a conexão
        client_socket.close()
        return data_received
    
def sent_message(message):
    """Envia uma mensagem para o servidor
    Returns:
        Retorna True caso todos os bytes tenham sido enviados ou False caso contrário
    """
    success = False
    # Inicializa o cliente
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((HOST, PORT))
        print("Conexão estabelecida com a Raspberry Pi")
        sent_bytes = client_socket.send(message.encode())
        # Verifica todos os bytes foram transmitidos
        if sent_bytes == len(message):
            success = True
    except Exception as e:
        print(e)
    finally:
        # Encerra a conexão
        client_socket.close()
        return success