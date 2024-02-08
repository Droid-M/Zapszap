# Importando módulos necessários
from DAOs import partnerDAO, groupDAO
from helpers import file, client, socket, socket
from services import partner_service as p_svc
from globals.variables import Group
# import copy

# Função para fazer solicitações de grupo
def make_group_request(message, host, port=None):
    # Conectando ao servidor do parceiro
    if port is None:
        port = file.env('DEFAULT_PARTNER_PORT')
    client_socket = client.connect_to_server(host, port)
    
    # Registrando o parceiro e enviando a mensagem
    partnerDAO.register(host, port, client_socket)
    socket.send_message(client_socket, message)
    
    # Descomente as linhas abaixo se desejar verificar a resposta do servidor
    # response = socket.receive_json_message(client_socket)
    # if not response.get('success'):
    #     raise Exception("\nFalha ao solicitar a conexão de grupo!\n")
    # return response.get('data')

# Função para solicitar conexão de grupo
def request_group_connection(host, port=None):
    return make_group_request({"code": "0X01"}, host, port)

# Função para enviar convite para novo grupo
def sent_new_group_invite(host, group: Group, port=None):
    return make_group_request({"code": "0X03", "group": group.to_dict()}, host, port)

# Função para registrar conexões de grupos
def register_groups_connection(groups: dict[str, dict]):
    for i in groups:
        groupDAO.register(groups[i]['name'], groups[i]['id'], groups[i]['members'])

# Função para obter informações sobre conexões de grupos
def return_group_connection():
    # groups = copy.deepcopy(groupDAO.GROUPS)
    return groupDAO.GROUPS

# Função para enviar mensagem para todos os membros do grupo
def send_group_message(group: groupDAO.Group, message, is_json=True):
    first_member = group.members[next(iter(group.members))]
    next_member = first_member.next_partner
    
    # Enviando mensagem para todos os membros do grupo
    p_svc.send_message(first_member, message, is_json)
    while next_member is not None:
        p_svc.send_message(next_member, message, is_json)
        next_member = next_member.next_partner

# Função para ingressar em um grupo
def join_in_group(group: groupDAO.Group):
    # Enviando mensagem para os membros do grupo informando a entrada
    send_group_message(group, {
        'code': '0X02',
        'group_id': group.id,
        'new_member_id': client.get_local_ip()
    })
