from helpers import input as InputHelper, client
from services import partner_service as p_svc, group_service as g_svc, data_service
from globals.variables import GROUPS, Group
from DAOs import groupDAO, partnerDAO
import time

def join_in_group():
    host = InputHelper.input_ip("Digite um endereço IP: ")
    count = 1
    available_groups: dict[str, Group] = {}
    #DOUBT - Require port too?
    groups = g_svc.request_group_connection(host)
    g_svc.register_groups_connection(groups)
    if len(GROUPS) == 0:
        print(f"Nenhum grupo obtido de {host}!")
        return
    print(f"Grupos de {host} consultados com sucesso!\n")
    print("Grupos disponíveis para ingressar:\n")
    for i in GROUPS:
        if not GROUPS[i].joined:
            print(f"\t{count} -- {GROUPS[i].name}_{GROUPS[i].id}")
        available_groups[count] = GROUPS[i]
        count += 1
    selected_group = InputHelper.input_integer("Informe o número correspondente ao grupo que você participar: \n")
    while (selected_group < 1) or selected_group > count:
        print("Opção inválida!")
        selected_group = InputHelper.input_integer("Informe o número correspondente ao grupo que você participar: \n")
    selected_group = available_groups[selected_group]
    g_svc.join_in_group(selected_group)
    data_service.backup_data()
    

def create_group():
    group_name = input("Insira o nome para o novo grupo: ")
    while len(group_name) < 1:
        group_name = input("Nenhum nome foi informado! insira o nome para o novo grupo: ")
    host = InputHelper.input_ip("Insira o endereço IP do primeiro membro que você quer adicionar ao grupo: ")
    local_ip = client.get_local_ip()
    group = groupDAO.register(group_name, int(time.time()), {
        local_ip : partnerDAO.get(local_ip), # O primeiro membro do grupo deve ser quem o criou
        # host :  partnerDAO.get(host)
    })
    g_svc.sent_new_group_invite(host, group)
    group.insert_member(partnerDAO.get(host))
    print("Solicitação enviada com sucesso! Em breve, o novo participante deve estar incluso no seu grupo.")
    data_service.backup_data()


def interact_with_groups():
    if len(GROUPS):
        print("Seus grupos:")
        for g in GROUPS.values():
            print(f"{g.name} - {g.id}")
        ipt2 = InputHelper.input_integer("Selecione uma opção\n1 - Consultar lista de membros de um grupo\n2 - Enviar mensagens para um grupo\nSua escolha: ")
        while ipt2 < 1 or ipt2 > 2:
            ipt2 = InputHelper.input_integer("Opção inválida! Selecione uma opção:\n1 - Consultar lista de membros de um grupo\n2 - Enviar mensagens para um grupo\nSua escolha: ")
        group_id = input("Informe o ID do grupo: ")
        while GROUPS.get(group_id) is None:
            group_id = input("O ID informado não pertence a nenhum dos grupos! Informe novamente o ID: ")
        group = GROUPS.get(group_id)
        if ipt2 == 1:
            for member in group.members.values():
                print(f"ID do membro: {member.host}")
        else:
            print("Envio de mensagens ainda não está disponível... :(")
    else:
        print("Você não possui grupos registrados!")