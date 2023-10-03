import socket

INTERNAL_ERROR_STATUS = "500"
SUCCESS_STATUS = "200"

def treat_message(message):
    return True

def handle_request(client_socket):
    message = ''
    try:
        message = SUCCESS_STATUS if treat_message(client_socket.recv(1024).decode()) else INTERNAL_ERROR_STATUS
    except Exception as e:
        print(f"Algum erro aconteceu: {e}")
        message = INTERNAL_ERROR_STATUS
    finally:
        client_socket.send(message.encode())
        client_socket.close()

def scan_local_network_ips(ip_range, on_present_device, on_absent_device, max_ip = 255):
    for i in range(0, max_ip):
        ip = f"{ip_range}.{i}"
        try:
            socket.gethostbyaddr(ip)
            on_present_device(ip)        
        except socket.herror:
            on_absent_device(ip)        
            pass