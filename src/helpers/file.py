from pathlib import Path

env_path = Path(__file__).parent.parent.__str__() + '/config.env'

def env(key, default_value = None):
    """Vasculha o arquivo de ambientação ('.env') à procura de alguma chave que corresponda à informada e retorna o valor atribuído a essa chave 
    Args: 
        key: Chave cujo valor atribuído no arquivo de ambientação deve ser obtido
        default_value: Valor a ser retornado caso a chave informada não seja localizada no arquivo .env
    """
    with open(env_path, "r") as env_file:
        env_vars = env_file.readlines()

    # Percorre as variáveis de ambiente e procura pela chave (key) informada
    for env_var in env_vars:
        if env_var.startswith(f'{key}='):
            return env_var.split("=")[1].strip().strip('"')
    return default_value