# Importando módulos necessários
from DAOs import partnerDAO, messageDAO
from helpers import client, file, socket, key
from globals import variables
from globals.variables import MY_IP
import time
import json

# Definindo nomes de arquivos para backups
MESSAGE_BACKUP_FILE = 'messages.zap'
PARTNERS_BACKUP_FILE = 'partners.zap'
FIRST_PARTNER_BACKUP_FILE = 'first_p.zap'

# Função para fazer backup dos dados
def backup_data():
    file.write_backup_file(MESSAGE_BACKUP_FILE, messageDAO.to_json())
    file.write_backup_file(PARTNERS_BACKUP_FILE, partnerDAO.to_json())
    file.write_backup_file(FIRST_PARTNER_BACKUP_FILE, variables.FIRST_PARTNER.to_json())

# Função para restaurar dados a partir de backups
def restore_data():
    # Lendo dados dos arquivos de backup
    msgData = file.read_backup_file(MESSAGE_BACKUP_FILE)
    partnersData = file.read_backup_file(PARTNERS_BACKUP_FILE)
    firstPData = file.read_backup_file(FIRST_PARTNER_BACKUP_FILE)
    
    # Restaurando mensagens, parceiros e o primeiro parceiro
    if msgData:
        variables.MESSAGES = messageDAO.from_list_of_dicts(msgData)
    if partnersData:
        variables.PARTNERS = partnerDAO.from_dict_of_dicts(partnersData)
        if firstPData:
            # partnerDAO.set_first(partnerDAO.from_dict(firstPData))
            partnerDAO.set_first(partnerDAO.get(firstPData.get("host")))
    
    # Registra chaves estrangeiras:
    me = partnerDAO.get_me()
    private_key = file.read_backup_file("private_key.zap")
    public_key = file.read_backup_file("public_key.zap")
    
    # Verificando e gerando um novo par de chaves se necessário
    if private_key is None and private_key is None:
        public_key, private_key = key.generate_key_pair()
    me.public_key = client.serialize_key(public_key, False)
    
    # Atualizando backups com as chaves e dados modificados
    file.write_backup_file(PARTNERS_BACKUP_FILE, partnerDAO.to_json())
    file.write_backup_file(FIRST_PARTNER_BACKUP_FILE, variables.FIRST_PARTNER.to_json())
    file.write_backup_file("public_key.zap", public_key)
    file.write_backup_file("private_key.zap", private_key)

# Função para sincronizar dados com outros parceiros
def sync_data():
    partner = partnerDAO.get_my_next_partner()
    
    # Enviando mensagens de sincronização, se houver um parceiro válido
    if partner:
        socket.send_message_to_online_partner(partner, {'code': 'Zx01', "new_partner_host": MY_IP})
        time.sleep(3)
        messages = key.encrypt_message(json.dumps(messageDAO.to_list_of_dicts()), partner.public_key)
        socket.send_message_to_online_partner(partner, {'code': 'Zx11', 'merge_messages': 1, "from": MY_IP,  'messages_list': messages, "sender": partnerDAO.get_me().name})
        time.sleep(3)

def set_username(name: str):
    partnerDAO.get_me().name = name
    backup_data()
    
def check_username(name: str):
    me = partnerDAO.get_me()
    return (str(me.name) == '') or name == me.name