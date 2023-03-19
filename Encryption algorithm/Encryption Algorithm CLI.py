import base64
import os
from Cryptodome.Cipher import AES

# Prompt the user for a message and a password
message = input("Enter a message to encrypt: ")
password = input("Enter a password: ")

# Convert the password to bytes and use it as the key for AES
key = password.encode()

# Generate a random initialization vector (IV)
iv = os.urandom(AES.block_size)

# Create a new AES cipher object in CBC mode
cipher = AES.new(key, AES.MODE_CBC, iv)

# Encrypt the message
ciphertext = cipher.encrypt(bytes(message, 'utf-8'))

# Encode the ciphertext and IV as base64 strings
ciphertext_b64 = base64.b64encode(ciphertext).decode()
iv_b64 = base64.b64encode(iv).decode()

# Display the encrypted message
print(f"Encrypted message: {ciphertext_b64}")
print(f"IV: {iv_b64}")

# To decrypt the message, we need to recreate the cipher object
# using the same key and IV
cipher = AES.new(key, AES.MODE_CBC, iv)

# Decrypt the ciphertext
plaintext = cipher.decrypt(ciphertext)

# Display the decrypted message
print(f"Decrypted message: {plaintext.decode('utf-8')}")