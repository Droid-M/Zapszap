# from globals.variables import Partner, PARTNERS, FIRST_PARTNER, MY_IP, FIRST_PART_REFERENCE
from helpers import file
from globals import variables
import json
from models.partner import Partner

def register(host, port, socket = None, public_key: str = None, is_offline: bool = False, name = ""):
    # global FIRST_PARTNER, PARTNERS

    # Verifica se o IP já está na lista
    partner = variables.PARTNERS.get(host)
    if partner is not None:
        if public_key:
            partner.public_key = public_key
            partner.is_offline = is_offline
        return partner

    # Cria uma nova instância de Partner
    new_partner = variables.Partner(host, port, socket, public_key=public_key, is_offline=is_offline, name=name)
    variables.PARTNERS[host] = new_partner
    # Insere e ordena com base no IP
    if variables.FIRST_PARTNER is None or host < variables.FIRST_PARTNER.host:
        new_partner.next_partner = variables.FIRST_PARTNER
        variables.FIRST_PARTNER = new_partner
    else:
        current = variables.FIRST_PARTNER
        while current.next_partner is not None and host > current.next_partner.host:
            current = current.next_partner
        new_partner.next_partner = current.next_partner
        current.next_partner = new_partner
    variables.FIRST_PART_REFERENCE[0] = variables.FIRST_PARTNER
    return new_partner

def get(host):
    return variables.PARTNERS.get(host)

def get_me():
    return get(variables.MY_IP)

def to_json():
    return json.dumps(to_dict(), indent=2)
    # partners = {}
    # for i in variables.PARTNERS:
    #     partners[i] = variables.PARTNERS[i].to_json()
    # return partners

def to_dict():
    partners = {}
    for i in variables.PARTNERS:
        partners[i] = variables.PARTNERS[i].to_dict()
    return partners

def from_dict(data: dict) -> variables.Partner:
    partner_instance = variables.Partner(data.get('host'), data.get('port'), data.get('socket'), data.get("public_key"))

    # Define outros atributos conforme necessário
    partner_instance.has_disconnected = data.get('has_disconnected', False)
    partner_instance.is_offline = data.get('is_offline', False)

    next_partner_data = data.get('next_partner')
    if next_partner_data:
        partner_instance.next_partner = from_dict(next_partner_data)
    return partner_instance

def from_dict_of_dicts(data: dict): 
    partners = {}
    for k, v in data.items():
        partners[k] = from_dict(v)
    return partners

def set_first(partner: Partner):
    variables.FIRST_PART_REFERENCE[0] = partner
    variables.FIRST_PARTNER = partner

def get_first():
    return variables.FIRST_PART_REFERENCE[0]
    partners_values = PARTNERS.values()
    return next(iter(partners_values)) if partners_values else None

def remove(host: str):
    # global FIRST_PARTNER, FIRST_PART_REFERENCE, PARTNERS

    current = get_first()
    previous = None

    # Procura o parceiro com o host fornecido
    while current is not None and current.host != host:
        previous = current
        current = current.next_partner

    # Se o parceiro não foi encontrado, retorna
    if current is None:
        file.log("server.log", "current é None")
        file.log("server.log", get_first().to_json())
        return

    # Remove o parceiro da lista encadeada
    if previous is None:
        variables.FIRST_PARTNER = current.next_partner
    else:
        previous.next_partner = current.next_partner

    # Remove o parceiro do dicionário PARTNERS
    del variables.PARTNERS[host]
    file.log("server.log", f"removendo {host}...\n")


    # Atualiza a referência do primeiro parceiro
    variables.FIRST_PART_REFERENCE[0] = variables.FIRST_PARTNER

    # Retorna o parceiro removido
    return current

def reset():
    me = get_me()
    me.next_partner = None
    me.is_offline - False
    variables.FIRST_PARTNER = me
    variables.FIRST_PART_REFERENCE[0] = me
    variables.PARTNERS = {me.host: variables.FIRST_PARTNER}
    file.log("server.log", "resetando...")

def empty():
    return len(variables.PARTNERS) == 0

def get_my_next_partner():
    partner = get_me().next_partner
    if partner is None and not empty():
        partner = get_first()
        while (partner is not None) and partner.host == variables.MY_IP:
            partner = partner.next_partner
    
    if (partner and partner.next_partner) and (partner.next_partner.host == partner.host) and partner.host == variables.MY_IP:
        return None
    return partner