import socket

# Obtém o endereço IP associado ao nome da máquina
ip_address = socket.gethostbyname("localhost")

def show():
    print("Zapszap - Versão 1.0\n\n")
    print(f"Endereço IP da máquina atual: {ip_address}")
    print("\nIndique a opção que deseja selecionar: ")
    print("1 - Consultar grupos disponíveis")
    print("2 - Participar de um grupo")
    print("3 - Sair de um grupo")
    print("4 - Criar um novo grupo")
    print("5 - Ler/enviar mensagens em um grupo")
