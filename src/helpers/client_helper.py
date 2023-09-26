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