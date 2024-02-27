from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
import base64

SYMMETRIC_KEY = b'\x00' * 32  # Chave AES de 256 bits preenchida com bytes nulos


def encrypt_data_with_rsa(public_key_pem):
    public_key = serialization.load_pem_public_key(public_key_pem.encode('utf-8'), backend=default_backend())
    encrypted_data = public_key.encrypt(
        SYMMETRIC_KEY,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    encrypted_data_base64 = base64.b64encode(encrypted_data).decode('utf-8')
    return encrypted_data_base64

def generate_rsa_key_pair():
    # Gerar uma chave RSA para criptografia assimétrica
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()

    # Serializar chaves para formato PEM (para armazenamento ou envio)
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return private_pem.decode('utf-8'), public_pem.decode('utf-8')

def generate_key_pair():
    private_key_pem, public_key_pem = generate_rsa_key_pair()
    return encrypt_data_with_rsa(public_key_pem), private_key_pem


def encrypt_message(data, public_key):
    # return message
    return encrypt_data_with_aes(data)

def decrypt_message(encrypted_message, private_key, public_key):
    # return encrypted_message
    decrypted_public_key = decrypt_data_with_rsa(public_key, private_key)
    return decrypt_data_with_aes(encrypted_message, decrypted_public_key)
    
def encrypt_data_with_aes(data):
    iv = os.urandom(16)  # Vetor de inicialização para AES
    padder = sym_padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data.encode('utf-8')) + padder.finalize()
    cipher = Cipher(algorithms.AES(SYMMETRIC_KEY), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    encrypted_iv_base64 = base64.b64encode(iv).decode('utf-8')
    encrypted_data_base64 = base64.b64encode(ciphertext).decode('utf-8')
    return encrypted_iv_base64 + encrypted_data_base64

def decrypt_data_with_rsa(encrypted_data, private_key_pem):
    private_key = serialization.load_pem_private_key(private_key_pem.encode('utf-8'), password=None, backend=default_backend())
    decrypted_data = private_key.decrypt(
        base64.b64decode(encrypted_data.encode('utf-8')),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted_data

def decrypt_data_with_aes(encrypted_data, key):
    iv = base64.b64decode(encrypted_data[:24])  # IV tem tamanho fixo de 16 bytes (24 bytes após codificação base64)
    ciphertext = base64.b64decode(encrypted_data[24:])
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = sym_padding.PKCS7(algorithms.AES.block_size).unpadder()
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
    return unpadded_data.decode('utf-8')