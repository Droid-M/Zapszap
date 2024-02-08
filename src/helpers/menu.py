import os
import sys
import subprocess
from datetime import datetime
from helpers import server

def restart():
    """Reinicia a aplicação"""
    if input("Tem certeza que deseja reiniciar o programa (Insira 'Y' para confirmar)? ").upper() == 'Y':
        print("Reiniciando programa...")
        server.stop()
        if os.name == 'nt':
            # Se estiver no Windows, use CREATE_NEW_CONSOLE para executar em um novo terminal CMD
            command = [sys.executable] + sys.argv
            subprocess.Popen(command, creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            # Se estiver em outra plataforma, apenas execute novamente o programa no mesmo terminal, limpando as saídas do programa anterior
            clear_console()
            os.execv(sys.executable if sys.executable else '/usr/bin/python3', ['python'] + sys.argv)
        sys.exit()
    else:
        print("Operação cancelada!")

def close(force_exit = True):
    """Encerra o programa"""
    if input("Tem certeza que deseja sair do programa (Insira 'Y' para confirmar)? ").upper() == 'Y':
        print("Saindo do programa...")
        if force_exit:
            exit()
        return True
    else:
        print("Operação cancelada!")
    return False

def clear_console():
    """ "Limpa" o terminal """
    os.system('cls' if os.name == 'nt' else 'clear')

def scroll_console(lines = 10):
    """Realiza uma pseudo-limpeza do console, exibindo linhas em branco até que o conteúdo anterior não esteja mais visível"""
    for _ in range(lines):
        print()

def pause():
    """Realiza um pseudo-bloqueio no programa até o usuário pressionar a teclar Enter para continuar o fluxo"""
    return input("Pressione Enter para continuar...")

def float_to_currency(value):
    """Formata qualquer valor do tipo ponto flutuante para o tipo moeda BRL (R$ XX,XX). Exemplo: '7.39' se torna 'R$ 7,39' """
    return f'R$ {value:.2f}'.replace('.', ',')