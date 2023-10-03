from backend import server
from frontend import main_menu, event_messages
from helpers import socket, file
import threading

present_network_ips = []

def on_present_device(ip):
    present_network_ips.append(ip)
    event_messages.on_present_device_in_network_message(ip)

def on_absent_device(ip):
    event_messages.on_absent_device_in_network_message(ip)

if __name__ == '__main__':
    server_service = threading.Thread(target=server.start)
    server_service.start(event_messages.waiting_new_connection_message, event_messages.new_client_connected_message, event_messages.socket_server_interrupted_message)
    event_messages.on_start_ip_search_message()
    socket.scan_local_network_ips(
        file.env('IP_RANGE', '192.168.0'),
        on_present_device,
        on_absent_device,
        file.env('MAX_DEVICE_QTY', 255)
    )
    main_menu.show()