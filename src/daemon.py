from helpers import server, file
from services import data_service as data_svc

CLIENTS = {}
HOST = "localhost"
PORT = int(file.env("SOCKET_PORT", 8050))

if __name__ == '__main__':
    # Restaura as mensagens e contatos anteriores
    data_svc.restore_data()

    # Sincroniza os dados com outros parceiros
    data_svc.sync_data()
    
    # Permite que o servidor seja iniciado em loop:
    file.delete_file('stop.z', True)

    server.start()