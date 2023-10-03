from backend import server
from frontend import main_menu
from frontend import event_messages
import threading

if __name__ == '__main__':
    server_service = threading.Thread(target=server.start)
    server_service.start(event_messages.waiting_new_connection_message, event_messages.new_client_connected_message, event_messages.socket_server_interrupted_message)
    main_menu.show()