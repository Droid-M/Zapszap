from helpers import input as InputHelper, menu, client, server
from controllers import group_controller
from services import partner_service, message_service

exit_menu = False

def read_input():
    global exit_menu
    ipt = InputHelper.choice("Sua escolha: ", InputHelper.input_integer, [1, 2, 3, 4, 5, 6])
    menu.scroll_console()
    if ipt == 1:
        host = InputHelper.input_ip("Informe o IP do seu colega: ")
        partner_service.start_partner_connection(host)
    elif ipt == 2:
        message_service.see_chat()
    elif ipt == 3:
        partner_service.list_partners()
    elif ipt == 4:
        partner_service.exit_group()
    elif ipt == 6:
        menu.restart()
    # elif ipt == 7: #FIXME - Remover esta opção
    #     message_service.send_group_message()
    else:
        exit_menu = menu.close(False)

def show():
    global exit_menu
    menu.scroll_console()
    try:
        while not exit_menu:
            print("Zapszap - Versão 1.0\n\n")
            print(f"Endereço IP da máquina atual: {client.get_local_ip()}")
            print("\nIndique a opção que deseja selecionar")
            print("1 - Conectar-se a um colega\n2 - Visualizar chat\n3 - Visualizar lista de colegas\n4 - Sair do grupo\n5 - Sair da aplicação\n6 - Reiniciar aplicação")
            # print("7 - escrever mensagem (deve ser removida)") #FIXME - Remover esta linha
            read_input()
    except Exception as e:
        print(f"Ops, algum erro aconteceu :(. Mensagem: {e}")
        menu.scroll_console(7)

    