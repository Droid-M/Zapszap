import re

def input_integer(message):
    """Exige que o usuário insira um valor inteiro enquanto não estiver dentro dos parâmetros esperados"""
    number = input(message)
    try:
        return int(number)
    except ValueError:
        print("Entrada inválida! Insira apenas valors numéricos inteiros!")
        # Exige novamente a inserção de um valor correto
        return input_integer(message)
    
def input_number(message):
    """Exige que o usuário insira um valor de ponto flutuante enquanto não estiver dentro dos parâmetros esperados"""
    number = input(message)
    try:
        return float(number)
    except ValueError:
        print("Entrada inválida! Insira apenas valors numéricos!")
        # Exige novamente a inserção de um valor correto
        return input_number(message)

def input_cpf(message):
    """Exige que o usuário insira um CPF válido enquanto nenhum for fornecido"""
    # Extrai apenas os números
    cpf = re.sub(r'[^0-9]', '', input(message))

    if len(cpf) != 11: #Se a quantidade de números não for 11, então o CPF é inválida:
        print("CPF inválido!")
        # Exige novamente a inserção de um CPF válido
        return input_cpf(message)

    if cpf == cpf[0] * 11: # Se os onze dígitos forem 0, então o CPF é inválida:
        print("CPF inválido!")
        # Exige novamente a inserção de um CPF válido
        return input_cpf(message)

    # Validando a "paridade" dos dígitos:
    total = 0
    for i in range(9):
        total += int(cpf[i]) * (10 - i)
    remainder = total % 11
    digit1 = 0 if remainder < 2 else 11 - remainder

    total = 0
    for i in range(10):
        total += int(cpf[i]) * (11 - i)
    remainder = total % 11
    digit2 = 0 if remainder < 2 else 11 - remainder

    if int(cpf[9]) == digit1 and int(cpf[10]) == digit2: # Se o penúltimo e antepenúltimo digito corresponderem à "verificação de paridade", então o CPF é válido:
        return cpf
    else:
        print("CPF inválido!")
        # Exige novamente a inserção de um CPF válido
        return input_cpf(message)