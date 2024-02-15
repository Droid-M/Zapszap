from DAOs import partnerDAO, groupDAO, messageDAO
from helpers import file, client, socket, time as TimeHelper, key
from globals.variables import Partner, MY_IP
from globals import variables
import json
from services import data_service

def close_all_connections():
    for i in variables.PARTNERS:
        partner = variables.PARTNERS[i]
        if partner.socket and not partner.has_disconnected:
            client.disconnect_client(partner.socket)
            partner.has_disconnected = True
    
def forward_message_to_active_member(partner: Partner, data: dict, is_json = True, stop_if_me = True):
    receivers_list: list = data.get("receivers_list", [])
    
    if len(variables.PARTNERS.keys()) <= 0:
        return False
    
    # all_as_received = len(partnerDAO) <= 1 and ((partnerDAO.get_first() is None) or partnerDAO.get_first().host == MY_IP)
    all_as_received = True

    # Se a quantidade de colegas que receberam a mensagem for igual ou superior à quantidade de colegas registrados, então verifique
    # se todos os colegas receberam (estão na lista de receptores)
    # if len(receivers_list) >= len(partnerDAO.PARTNERS): # REVIEW - remover esta linha depois
    
    for host in variables.PARTNERS.keys():
        if host not in receivers_list:
            all_as_received = False
            break
        
    if all_as_received: # Se todos receberam a mensagem, então não há porque continuar esta tarefa e o fluxo é interrompido
        file.log("server.log", "todos receberam")
        return True
    
    # O próximo parceiro a receber a mensagem é o primeiro que ainda não está na lista dos que já receberam:
    partner = partnerDAO.get(host)

    #Enquanto uma dessas condições não forem cumpridas, envie mensagem para o proximo parceiro:
    #   1 - O IP de quem deve receber não for o do próprio computador que está enviando
    #   2 - Houver um próximo parceiro na lista para receber a mensagem
    #   3 - O próximo parceiro na lista conseguir receber a mensagem com sucesso
    return socket.send_message_to_online_partner(partner, data, is_json, stop_if_me)
    
def start_partner_connection(host):
    partner = Partner(host, int(file.env('DEFAULT_PARTNER_PORT')))
    me = partnerDAO.get_me()
    if socket.send_message_to_partner(partner, {'code': 'Zx01', "new_partner_host": MY_IP, 'new_partner_public_key': me.public_key}):
        # Aqui, o parceiro irá corresponder enviando seus próprios dados, por isso partnerDAO.get(host) irá retornar a instancia do parceiro com dados atualizados
        TimeHelper.regressive_counter(4)
        partner = partnerDAO.get(host)
        if (partner is None):
            print("\nO parceiro não respondeu à sua solicitação!\n")
            return
        messages = key.encrypt_message(json.dumps(messageDAO.to_list_of_dicts()), partner.public_key)
        socket.send_message_to_partner(partner, {'code': 'Zx11', 'merge_messages': 1, "from": MY_IP,  'messages_list': messages, "sender": me.name})
        print("Solicitação de conexão enviada com sucesso!")
    else:
        print("Solicitação de conexão falhou!")

def receive_partners_list(partner_chained_list: Partner):
    while partner_chained_list is not None:
        partnerDAO.register(
            partner_chained_list.host, 
            partner_chained_list.port, 
            None,
            partner_chained_list.public_key,
            partner_chained_list.is_offline,
            partner_chained_list.name
        )
        partner_chained_list = partner_chained_list.next_partner

def list_partners():
    current = partnerDAO.get_first()
    file.log("server.log", "listando")
    count = 1
    if current.host == MY_IP and current.next_partner is None:
        print("Nenhum colega atualmente registrado!")
    else:
        print("Colegas conectados: ")
        while current is not None:
            if current.host != MY_IP:
                print(count, "-", current.host)
                count += 1
            current = current.next_partner

def exit_group():
    if forward_message_to_active_member(partnerDAO.get_first(), {'code': 'Zx02', "host_to_remove": MY_IP}):
        TimeHelper.regressive_counter(4)
        partnerDAO.reset()
        data_service.backup_data()
        print("Solicitação de desconexão enviada com sucesso!")
    else:
        print("Falha ao tentar desconectar-se do grupo! Tente novamente mais tarde.")