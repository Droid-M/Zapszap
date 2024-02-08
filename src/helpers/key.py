from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
import json
import base64

def generate_key_pair():
    # Gera um par de chaves RSA
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    # Obtém a chave pública em formato PEM
    public_key = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode('utf-8')

    # Obtém a chave privada em formato PEM
    private_key_str = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    ).decode('utf-8')

    return public_key, private_key_str

def encrypt_message(message: str, public_key: str):
    return message
    try:
        # Carregar a chave pública
        public_key_bytes = public_key.encode('utf-8')
        public_key_obj = serialization.load_pem_public_key(public_key_bytes, backend=default_backend())

        # Criptografar a string JSON
        ciphertext = public_key_obj.encrypt(
            message.encode('utf-8'),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # Retornar o JSON criptografado como bytes
        return base64.b64encode(ciphertext).decode('utf-8')
    except Exception as e:
        print(f"Erro ao carregar a chave pública: {e}")
        print(f"Chave Pública: {public_key}")
        print(f"Mensagem: {message}")
        raise e
        return None

def decrypt_message(encrypted_message, private_key: str):
    return encrypted_message
    try:
        encrypted_message = base64.b64decode(encrypted_message)
        # Carregar a chave privada
        private_key_bytes = private_key.encode('utf-8')
        private_key_obj = serialization.load_pem_private_key(private_key_bytes, password=None, backend=default_backend())

        # Descriptografar o JSON
        decrypted_data = private_key_obj.decrypt(
            encrypted_message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # Converter os bytes descriptografados de volta para a string JSON
        decrypted_json = json.loads(decrypted_data.decode('utf-8'))

        return decrypted_json
    except Exception as e:
        return encrypted_message.decode()

# def decrypt_json_message(cipher_text, private_key):
#     n, d = private_key
#     # Convertendo bytes para string
#     cipher_text_str = cipher_text.decode('utf-8')
#     # Tentando analisar a string como JSON
#     try:
#         json_data = json.loads(cipher_text_str)
#         # Se bem-sucedido, retornar o JSON
#         return json_data
#     except json.JSONDecodeError:
#         # Se falhar, continuar com a descriptografia
#         pass

#     # Separando os números da string
#     cipher_numbers = cipher_text_str.split()
#     # Decifrando cada número
#     decrypted_text = ''.join([chr(pow(int(char), d, n)) for char in cipher_numbers])
    # return decrypted_text


def mask_message(message, key):
    encrypted = []

    for i in range(len(message)):
        # Aplica o operador XOR para cada caractere da mensagem e da chave
        encrypted_char = chr(ord(message[i]) ^ ord(key[i % len(key)]))
        encrypted.append(encrypted_char)

    # Converte a mensagem cifrada para representação hexadecimal
    encrypted_hex = ''.join([format(ord(char), 'x') for char in encrypted])

    return encrypted_hex

def unmask_message(encrypted_hex, key):
    # Converte a representação hexadecimal de volta para a mensagem cifrada
    encrypted = [chr(int(encrypted_hex[i:i+2], 16)) for i in range(0, len(encrypted_hex), 2)]

    decrypted = []

    for i in range(len(encrypted)):
        # Aplica o operador XOR inverso para cada caractere da mensagem cifrada e da chave
        decrypted_char = chr(ord(encrypted[i]) ^ ord(key[i % len(key)]))
        decrypted.append(decrypted_char)

    # Retorna a mensagem decifrada como uma string
    return ''.join(decrypted)