import socket
import time
from services import data_service
from helpers import file

stayed_offline = False

def is_online():
    try:
        # Tenta criar um socket para um servidor conhecido (como um servidor DNS do Google)
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except OSError:
        pass
    return False

def check_network():
    global stayed_offline
    while True:
        if is_online():
            file.log("network.log", "is Online")
            if stayed_offline:
                data_service.sync_data()
                stayed_offline = False
        elif not stayed_offline:
            file.log("network.log", "is Offline")
            print("\nVocê está Offline!\n")
            stayed_offline = True
        time.sleep(5)  # Verifica a cada 5 segundos