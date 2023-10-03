import server
import threading

if __name__ == '__main__':
    server_service = threading.Thread(target=server.start)
    server_service.start()