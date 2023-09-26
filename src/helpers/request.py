import requests
from helpers import file
import uuid

BASE_URL = file.env("API_URL")

def get_mac_address():
    # função criada base em "www.codespeedy.com/how-to-get-mac-address-of-a-device-in-python"
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ':'.join([mac[i:i+2] for i in range(0, 12, 2)])

def is_success(response):
    """Informa se a requisição teve status de sucesso (entre 100 e 399) ou não"""
    return response.status_code >= 100 and response.status_code < 400

def get(endpoint, headers, body = {}, query = {}):
    return requests.get(BASE_URL + "/" + endpoint, data = body, params = query, headers = headers)

def post(endpoint, headers, body = {}, query = {}):
    return requests.post(BASE_URL + "/" + endpoint, json = body, params = query, headers = headers)

def render_response_message(response):
    """Exibe a mensagem contida na requisição.
    Em caso de status 422 na requisição, as mensagens de erro de validação contidas no corpo da resposta serão exibidas também
    """
    message = response.json().get("message")
    if message:
        print(message)
    else:
        print("Sucesso na requisição!" if is_success(response) else "Falha na requisição")
    if (response.status_code == 422):
        errors = response.json().get('errors', [])
        if isinstance(errors, dict):
            for i in errors:
                print(f"{i}: {errors[i]}")
        elif isinstance(errors, list):
            for i in errors:
                print(i)
    
