from helpers import file
import main_menu
from services import data_service as data_svc
import sys

CLIENTS = {}
HOST = "localhost"
PORT = int(file.env("SOCKET_PORT", 8050))

if __name__ == '__main__':
    if (len(sys.argv) < 3):
        exit("\nQuantidade de argumentos inválidos! O mínimo requerido são 2 (main.py {user} {command} {optional:content}) conforme o exemplo: main.py Marcos read-messages")
    
    # Restaura as mensagens e contatos anteriores
    data_svc.restore_data()

    if data_svc.check_username(sys.argv[1]):
        data_svc.set_username(sys.argv[1])
        content = None
        if (len(sys.argv) > 3):
            content = sys.argv[3]
        main_menu.run(sys.argv[2], content)
    else:
        print("ERROR: Nome de usuário informado não corresponde ao usuário conectado! Se deseja usar outro username, primeiro faça LOGOFF da conta atualmente conectada.")