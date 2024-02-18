from pathlib import Path
import os
import datetime
import json
from typing import Union
from helpers import type

BASE_PATH = Path(__file__).parent.parent.__str__()
ENV_PATH = BASE_PATH + '/config.env'

def split_path(file_path):
    # Get the file name and directory name
    file_name = os.path.basename(file_path)
    directory_name = os.path.dirname(file_path)
    return file_name, directory_name

def env(key, default_value = None):
    """Vasculha o arquivo de ambientação ('.env') à procura de alguma chave que corresponda à informada e retorna o valor atribuído a essa chave 
    Args: 
        key: Chave cujo valor atribuído no arquivo de ambientação deve ser obtido
        default_value: Valor a ser retornado caso a chave informada não seja localizada no arquivo .env
    """
    with open(ENV_PATH, "r") as env_file:
        env_vars = env_file.readlines()

    # Percorre as variáveis de ambiente e procura pela chave (key) informada
    for env_var in env_vars:
        if env_var.startswith(f'{key}='):
            return env_var.split("=")[1].strip().strip('"')
    return default_value

def file_exists(file_path, using_absolute_path = False):
    if not using_absolute_path:
        return os.path.exists(BASE_PATH + '/' + file_path)
    return os.path.exists(file_path)

def delete_file(file_relative_path, quiet = True):
    try:
        os.remove(BASE_PATH + '/' + file_relative_path)
        if not quiet:
            print(f"Arquivo {file_relative_path} excluído com sucesso.")
    except FileNotFoundError:
        if not quiet:
            print(f"O arquivo {file_relative_path} não foi encontrado.")
    except Exception as e:
        if not quiet:
            print(f"Ocorreu um erro ao excluir o arquivo: {e}")

def create_file(file_relative_path, content = '', quiet = True):
    try:
        with open(BASE_PATH + '/' + file_relative_path, 'w') as file:
            file.write(content)
        if not quiet:
            print(f"Arquivo {file_relative_path} criado com sucesso.")
    except Exception as e:
        if not quiet:
            print(f"Ocorreu um erro ao criar o arquivo: {e}")

def log(file_relative_path: str, message: str):
    timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S.%f]")[:-3]
    directory = BASE_PATH + '/logs/'
    os.makedirs(directory, exist_ok=True)
    with open(BASE_PATH + '/logs/' + file_relative_path, "a"):
        pass
    with open(BASE_PATH + '/logs/' + file_relative_path, "a") as log_file:
        log_file.write(f"{timestamp} {message}\n")

def read_backup_file(file_relative_path)-> Union[dict, str, None]:
    file_relative_path = BASE_PATH + '/backups/' + file_relative_path
    try:
        # Verifica se o arquivo .zap existe
        if file_exists(file_relative_path, True):
            # Lê o conteúdo do arquivo .zap
            with open(file_relative_path, 'r') as file:
                content = file.read()

            if type.is_json_string(content):
                # Converte o conteúdo para JSON
                return json.loads(content)
            return content
        else:
            print(file_relative_path, "não existe!")
            # Retorna None se o arquivo não existir
            return None
    except Exception as e:
        # Trata exceções, se houver algum erro
        print(f"Ocorreu um erro ao ler o arquivo de backup: {e}")
        return None

def write_backup_file(file_relative_path, content, quiet=True):
    file_relative_path = BASE_PATH + '/backups/' + file_relative_path
    try:
        # Escreve o conteúdo no arquivo de backup
        with open(file_relative_path, 'w') as file:
            if isinstance(content, (dict, list)):
                # Se o conteúdo for um dicionário ou uma lista, converte para JSON antes de escrever
                content = json.dumps(content, indent=2)
            file.write(content)

        if not quiet:
            print(f"Arquivo de backup {file_relative_path} gerado com sucesso.")
    except Exception as e:
        if not quiet:
            print(f"Ocorreu um erro ao gerar o arquivo de backup: {e}")