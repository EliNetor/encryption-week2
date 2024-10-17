from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from shamir_mnemonic import combine_mnemonics

def recover_key(shares):
    flat_shares = [mnemonic for share_group in shares for mnemonic in share_group]
    recovered_key = combine_mnemonics(flat_shares)
    return recovered_key

def decrypt_message(encrypted_message, key):
    iv = encrypted_message[:16]
    ciphertext = encrypted_message[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
    return plaintext.decode()

if __name__ == "__main__":
    num_of_shares = int(input("number of shares (n): "))
    required_shares = int(input("required shares to recover the key (k): "))
    
    shares = []
    for i in range(num_of_shares):
        share = input(f"Enter share {i + 1}: ")
        shares.append([share])

    encrypted_message_hex = input("encrypted message: ")
    encrypted_message = bytes.fromhex(encrypted_message_hex)
    
    recovered_key = recover_key(shares)
    decrypted_message = decrypt_message(encrypted_message, recovered_key)
    print(f"Decrypted message: {decrypted_message}")
