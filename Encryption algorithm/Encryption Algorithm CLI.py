import base64
import os
from Cryptodome.Cipher import AES
import getpass

def encrypt_message(message: str, password: str) -> bytes:
    try:
        # Use a key derivation function to generate a key from the password
        salt = os.urandom(16)
        key = get_key(password, salt)

        # Generate a random initialization vector (IV)
        iv = os.urandom(AES.block_size)

        # Create a new AES cipher object in CBC mode
        cipher = AES.new(key, AES.MODE_CBC, iv)

        # Encrypt the message
        ciphertext = cipher.encrypt(bytes(message, 'utf-8'))

        # Encode the ciphertext and IV as base64 strings
        ciphertext_b64 = base64.b64encode(ciphertext).decode()
        iv_b64 = base64.b64encode(iv).decode()

        # Return the encrypted message, salt, and IV
        return b'%b:%b:%b' % (salt, iv_b64.encode(), ciphertext_b64.encode())

    except (ValueError, TypeError) as e:
        print(f"Error encrypting message: {e}")

def decrypt_message(encrypted_message: bytes, password: str) -> str:
    try:
        # Split the encrypted message into its components
        salt, iv_b64, ciphertext_b64 = encrypted_message.split(b':')

        # Use a key derivation function to generate a key from the password and salt
        key = get_key(password, salt)

        # Decode the IV and ciphertext from base64
        iv = base64.b64decode(iv_b64)
        ciphertext = base64.b64decode(ciphertext_b64)

        # Create a new AES cipher object in CBC mode
        cipher = AES.new(key, AES.MODE_CBC, iv)

        # Decrypt the message
        plaintext = cipher.decrypt(ciphertext)

        # Return the decrypted message
        return plaintext.decode('utf-8')

    except (ValueError, TypeError) as e:
        print(f"Error decrypting message: {e}")

def get_key(password: str, salt: bytes) -> bytes:
    # Use PBKDF2 to generate a key from the password and salt
    key = getpass.pbkdf2(password, salt, 100000, 32)
    return key

if __name__ == '__main__':
    # Prompt the user for a message and a password
    message = input("Enter a message to encrypt: ")
    password = getpass.getpass(prompt="Enter a password: ")

    # Encrypt the message
    encrypted_message = encrypt_message(message, password)
    print(f"Encrypted message: {encrypted_message}")

    # Decrypt the message
    decrypted_message = decrypt_message(encrypted_message, password)
    print(f"Decrypted message: {decrypted_message}")