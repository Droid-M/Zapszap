# def compare_dicts(old, new, watched_keys):
#     modified_values = {}
#     for key in watched_keys:
#         if key in old and key in new:
#             if old[key] != new[key]:
#                 modified_values[key] = (old[key], new[key])
#     return modified_values

def compare_dicts(old, new, watched_keys=None, current_key=''):
    """Compara dois dicionários com base nas chaves informadas e indica quais pares de atributo->valor mudaram"""
    modified_values = {}
    for key in old.keys():
        # Define a chave atual para comparação como a própria chave se ela não for aninhada, senão, usa sua subchave/subvalor
        current_nested_key = f"{current_key}.{key}" if current_key else key
        if watched_keys is None or current_nested_key in watched_keys: #Se ainda não houver valores diferentes registrados entre os dicionários, faça:
            if key in new:
                if isinstance(old[key], dict) and isinstance(new[key], dict):
                    # Se chave é um dicionário em ambos os dicionários, compare recursivamente.
                    nested_changes = compare_dicts(old[key], new[key], watched_keys, current_nested_key)
                    if nested_changes:
                        modified_values[key] = nested_changes
                elif old[key] != new[key]: #Se valor associado à chave é diferente, registre:
                    modified_values[key] = (old[key], new[key])
    for key in new.keys():
        current_nested_key = f"{current_key}.{key}" if current_key else key
        if watched_keys is None or current_nested_key in watched_keys:
            if key not in old: #Se o dicionário novo possuir chaves que não estão presentes no velho, registre:
                modified_values[key] = (None, new[key])
    return modified_values
