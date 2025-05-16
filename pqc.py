from kyber_py.kyber import Kyber512
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

def generate_keys():
    """
    Generate Kyber512 keypair.
    Returns:
        tuple: (public_key, private_key)
    """
    public_key, private_key = Kyber512.keygen()
    return public_key, private_key

def encrypt_message(public_key: bytes, message: str):
    """
    Encrypts a message using Kyber512 for key encapsulation and AES-CBC for symmetric encryption.

    Args:
        public_key (bytes): The recipient's Kyber public key.
        message (str): The plaintext message to encrypt.

    Returns:
        tuple: (kem_ciphertext, aes_ciphertext), where:
            - kem_ciphertext (bytes): Ciphertext from Kyber encapsulation.
            - aes_ciphertext (bytes): IV + AES-CBC encrypted message.
    """
    try:
        shared_secret, kem_ct = Kyber512.encaps(public_key)
    except Exception as e:
        raise ValueError(f"KEM encryption failed: {e}")

    aes_key = shared_secret[:32]  # AES-256 requires 32-byte key
    cipher = AES.new(aes_key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(message.encode(), AES.block_size))
    aes_cipher = cipher.iv + ct_bytes  # Prepend IV

    return kem_ct, aes_cipher

def decrypt_message(private_key: bytes, kem_ct: bytes, aes_cipher: bytes):
    """
    Decrypts a message using Kyber512 for key decapsulation and AES-CBC for symmetric decryption.

    Args:
        private_key (bytes): The recipient's Kyber private key.
        kem_ct (bytes): Ciphertext from Kyber encapsulation.
        aes_cipher (bytes): The AES encrypted message with IV prepended.

    Returns:
        str: The original plaintext message.
    """
    try:
        shared_secret = Kyber512.decaps(private_key, kem_ct)
    except Exception as e:
        raise ValueError(f"KEM decryption failed: {e}")

    aes_key = shared_secret[:32]
    iv = aes_cipher[:16]
    ct = aes_cipher[16:]

    try:
        cipher = AES.new(aes_key, AES.MODE_CBC, iv)
        decrypted_message = unpad(cipher.decrypt(ct), AES.block_size).decode()
    except Exception as e:
        raise ValueError(f"AES decryption failed: {e}")

    return decrypted_message
