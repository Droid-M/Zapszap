from helpers import menu
from services import partner_service, message_service

def run(command: str, content = None):
    command = command.lower()
    if command == 'connect':
        if (not content):
            exit('Ip do parceiro é obrigatório!')
        partner_service.start_partner_connection(content)
    elif command == 'read-messages':
        message_service.see_chat()
    elif command == 'list-partners':
        partner_service.list_partners()
    elif command == 'exit-group':
        partner_service.exit_group()
    elif command == 'send-message':
        if (not content):
            exit('ERROR: Conteúdo da mensagem é obrigatório!')
        message_service.send_group_message(content)
    else:
        print("ERROR: Comando inválido!")
        # exit_menu = menu.close(False)