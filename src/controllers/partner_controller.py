# from services.partner_service import *
from services import partner_service, data_service
from DAOs import partnerDAO
from helpers import file, client, socket, time as TimeHelper
from globals.variables import Partner, MY_IP


def remove_partner(data: dict):
    host_to_remove = data.get("host_to_remove")

    # Registra/mescla a lista de colegas enviados na mensagem:
    first = data.get("first_partner")
    if first:
        partner_service.receive_partners_list(partnerDAO.from_dict(first))

    # Registra que o usuário recebeu e tratou a mensagem:
    receivers_list: list = data.get("receivers_list", [])
    if MY_IP not in receivers_list:
        receivers_list.append(MY_IP)
    data["receivers_list"] = receivers_list

    # Remove da lista de parceiros IP que quer sair do grupo:
    if host_to_remove != MY_IP:
        partnerDAO.remove(host_to_remove)

    data["first_partner"] = partnerDAO.get_first().to_dict()
    next = partnerDAO.get_me().next_partner

    file.log("1.log", "remoção iniciada")

    # Se o próximo a receber a mensagem for quem iniciou o ciclo e este não for o ultimo na fila, então ignore-o caso o próximo da fila não houver recebido a msg:
    if next is not None and next.host == host_to_remove and next.next_partner is not None and next.next_partner not in receivers_list:
        next = next.next_partner

    # Envia a mensagem para o próximo colega na lista:
    if next is None:
        next = partnerDAO.get_first()
    file.log("1.log", next.to_json() if next else "Nada?!")
    data_service.backup_data()
    partner_service.forward_message_to_active_member(next, data)

def share_partner(data: dict):
    new_partner_host = data.get("new_partner_host")

    # Registra o IP da máquina que quer entrar no grupo:
    partnerDAO.register(new_partner_host, file.env('DEFAULT_PARTNER_PORT'), None, data.get("new_partner_public_key"))

    # Registra/mescla a lista de colegas enviados na mensagem:
    first = data.get("first_partner")
    if first:
        partner_service.receive_partners_list(partnerDAO.from_dict(first))

    # Registra que o usuário recebeu e tratou a mensagem:
    receivers_list: list = data.get("receivers_list", [])
    if MY_IP not in receivers_list:
        receivers_list.append(MY_IP)
    data["receivers_list"] = receivers_list

    me = partnerDAO.get_me()

    data["first_partner"] = partnerDAO.get_first().to_dict()

    next = me.next_partner

    # Se o próximo a receber a mensagem for quem iniciou o ciclo e este não for o ultimo na fila, então ignore-o caso o próximo da fila não houver recebido a msg:
    if next is not None and next.host == new_partner_host and next.next_partner is not None and next.next_partner not in receivers_list:
        next = next.next_partner

    # Envia a mensagem para o próximo colega na lista:
    if next is None:
        next = partnerDAO.get_first()
    data_service.backup_data()
    partner_service.forward_message_to_active_member(next, data)
