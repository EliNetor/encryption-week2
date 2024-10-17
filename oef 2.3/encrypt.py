from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os
from shamir_mnemonic import generate_mnemonics

def generate_aes_key():
    return os.urandom(32)

def split_key(key, n=2, k=2):
    groups = [(k, n)]
    shares = generate_mnemonics(1, groups, master_secret=key)
    return shares

def encrypt_message(message, key):
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(message.encode()) + padder.finalize()
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_message = encryptor.update(padded_data) + encryptor.finalize()
    return iv + encrypted_message

if __name__ == "__main__":
    aes_key = generate_aes_key()
    print(f"AES key: {aes_key.hex()}")
    shares = split_key(aes_key, n=2, k=2)
    print(f"Shared keys: {shares}")
    message = "encrypted message for lesson 2"
    encrypted_message = encrypt_message(message, aes_key)
    print(f"Encrypted message: {encrypted_message.hex()}")
