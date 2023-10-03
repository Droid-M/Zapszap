#SECTION - SOCKET SERVER
def waiting_new_connection_message():
    print("Aguardando conexões...")

def new_client_connected_message(client_address):
    print(f"Conexão estabelecida com {client_address}")

def socket_server_interrupted_message():
    print("Servidor interrompido pelo usuário.")
#!SECTION

#SECTION - SEARCH IP'S
def on_start_ip_search_message():
    print("Iniciando varredura de dispositivos na rede. Por favor, aguarde...")

def on_present_device_in_network_message(ip):
    print(f"{ip} - Presente na rede") 
 
def on_absent_device_in_network_message(ip):
    print(f"{ip} - Ausente na rede") 
#!SECTION