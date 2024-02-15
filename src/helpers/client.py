import socket
from helpers import socket as CustomSocket
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import base64
import requests
import netifaces

IP = None

def serialize_key(key, is_private):
    return key
    # if not is_private:
    #     key_bytes = key.public_bytes(
    #         encoding=serialization.Encoding.PEM,
    #         format=serialization.PublicFormat.SubjectPublicKeyInfo
    #     )
    # else:
    #     key_bytes = key.private_bytes(
    #         encoding=serialization.Encoding.PEM,
    #         format=serialization.PrivateFormat.PKCS8,
    #         encryption_algorithm=serialization.NoEncryption()
    #     )
    # return base64.b64encode(key_bytes).decode('utf-8')

def deserialize_key(key_str: str, is_private):
    return key_str
    # key_bytes = base64.b64decode(key_str.encode('utf-8'))
    # if not is_private:
    #     key = serialization.load_pem_public_key(
    #         key_bytes,
    #         backend=default_backend()
    #     )
    # else:
    #     key = serialization.load_pem_private_key(
    #         key_bytes,
    #         password=None,
    #         backend=default_backend()
    #     )
    # return key

# def encrypt_message(message, public_key):
#     ciphertext = public_key.encrypt(
#         message.encode('utf-8'),
#         padding.OAEP(
#             mgf=padding.MGF1(algorithm=hashes.SHA256()),
#             algorithm=hashes.SHA256(),
#             label=None
#         )
#     )
#     return ciphertext

# def decrypt_message(ciphertext, private_key):
#     plaintext = private_key.decrypt(
#         ciphertext,
#         padding.OAEP(
#             mgf=padding.MGF1(algorithm=hashes.SHA256()),
#             algorithm=hashes.SHA256(),
#             label=None
#         )
#     )
#     return plaintext.decode('utf-8')

def connect_to_server(host, port: int):
    port = int(port)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(5)
    client_socket.connect((host, port))
    return client_socket

def disconnect_client(client_socket, quiet = True):
    client_socket.close()
    if not quiet:
        print("Cliente desconectado.")

# def get_local_ip():
#     host_name = socket.gethostname()
#     local_ip = socket.gethostbyname(host_name)
#     return local_ip


def get_public_ip():
    global IP
    if IP is not None:
        return IP
    response = requests.get('https://api.ipify.org')
    if response.status_code == 200:
        IP = response.text
        return IP
    else:
        return "Erro ao obter o endereço IP público."
    
    
def get_local_ip():
    try:
        # Obtém a interface padrão do sistema
        default_interface = netifaces.gateways()['default'][netifaces.AF_INET][1]

        # Obtém o endereço IP associado à interface padrão
        ip_addresses = netifaces.ifaddresses(default_interface)[netifaces.AF_INET]
        ip_address = ip_addresses[0]['addr'] if ip_addresses else None
        return ip_address
    except (KeyError, ValueError):
        print("Erro ao obter o endereço IP da interface padrão na sua máquina.")
        return None
    
    
def get_local_ip_1():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    host_ip = s.getsockname()[0]
    s.close()
    return host_ip