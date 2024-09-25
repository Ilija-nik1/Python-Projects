"""
Steganography Program Instructions:

1. Purpose:
   This program allows you to hide (encode) a secret message inside an image and later retrieve (decode) the hidden message from the image.

2. Requirements:
   - Install the required libraries:
     - PIL (Pillow) for image processing: `pip install Pillow`
     - cryptography for encryption: `pip install cryptography`

3. Program Features:
   - The secret message is encrypted using AES-GCM encryption before being hidden in the image.
   - The key for encryption can either be generated or derived from a password.
   - You can save and load encryption keys securely.

4. How to use the program:
   - Encoding a message:
     1. Enter a password to derive the encryption key.
     2. Call `encode_message()` with an image file (e.g., 'input_image.png') and the message you want to hide.
     3. The program will save a new image (e.g., 'encoded_image.png') with the hidden message.

   - Decoding a message:
     1. Load the image with the hidden message (e.g., 'encoded_image.png').
     2. Call `decode_message()` to retrieve the hidden message.

5. Example steps:
   1. Run the program and provide a password when prompted.
   2. The program will save your key securely.
   3. Encode a message into an image by specifying the input image path and output image path.
   4. Decode the hidden message by providing the encoded image path.

6. Note:
   - The image used for encoding should have enough space to store the message. A very large message may not fit in a small image.
"""

from PIL import Image
import numpy as np
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
import base64
import random
import hashlib
import logging
import getpass

logging.basicConfig(level=logging.INFO)

class Steganography:
    def __init__(self, key=None, password=None, salt=None):
        """
        Initializes the Steganography object by generating or deriving a key.
        Key can be directly provided or derived from a password.
        """
        self.salt = salt or os.urandom(16)
        if password:
            self.key = self._derive_key_from_password(password)
        elif key:
            self.key = key.encode() if isinstance(key, str) else key
        else:
            self.key = AESGCM.generate_key(bit_length=256)

    def _derive_key_from_password(self, password):
        """Derives a key from the password using PBKDF2HMAC."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
            backend=default_backend()
        )
        return kdf.derive(password.encode())

    def _encrypt_message(self, message):
        """
        Encrypts the message and appends a checksum for integrity verification.
        Generates a unique nonce for each encryption operation.
        """
        aesgcm = AESGCM(self.key)
        nonce = os.urandom(12)  # Unique nonce per encryption
        checksum = hashlib.sha256(message.encode()).digest()
        encrypted_message = aesgcm.encrypt(nonce, message.encode() + checksum, None)
        encrypted_message_bits = ''.join([format(byte, '08b') for byte in nonce + encrypted_message])
        return encrypted_message_bits

    def _decrypt_message(self, binary_message):
        """
        Decrypts the binary message using the provided key and verifies integrity using checksum.
        Extracts nonce from the start of the binary_message.
        """
        byte_array = bytearray(int(binary_message[i:i+8], 2) for i in range(0, len(binary_message), 8))
        nonce, ciphertext = byte_array[:12], byte_array[12:]
        aesgcm = AESGCM(self.key)
        decrypted_message = aesgcm.decrypt(nonce, bytes(ciphertext), None)
        message, checksum = decrypted_message[:-32], decrypted_message[-32:]
        if hashlib.sha256(message).digest() != checksum:
            raise ValueError("Message integrity check failed.")
        return message.decode()

    def encode_message(self, image_path, message, output_image_path, random_seed=None):
        """
        Encodes an encrypted message into an image by modifying its least significant bits.
        A delimiter is added at the end of the message.
        """
        image = self._load_image(image_path)
        image_array = np.array(image)
        message_binary = self._encrypt_message(message)
        message_binary += '1111111111111110'  # Delimiter for the end of the message
        message_length = len(message_binary)

        flat_image_array = image_array.flatten()
        if message_length > len(flat_image_array):
            raise ValueError("Message is too long to be hidden in the image.")
        
        # Shuffle indices for random distribution of the message in the image
        indices = list(range(len(flat_image_array)))
        if random_seed is not None:
            random.seed(random_seed)
        random.shuffle(indices)
        selected_indices = indices[:message_length]

        for i, bit in zip(selected_indices, message_binary):
            flat_image_array[i] = (flat_image_array[i] & 254) | int(bit)

        # Reshape and save the new image
        encoded_image_array = flat_image_array.reshape(image_array.shape)
        encoded_image = Image.fromarray(encoded_image_array.astype('uint8'))
        encoded_image.save(output_image_path)
        logging.info(f"Message encoded and saved to {output_image_path}")

    def decode_message(self, image_path):
        """
        Decodes and decrypts a hidden message from the image.
        """
        image = self._load_image(image_path)
        flat_image_array = np.array(image).flatten()

        # Extract the binary message by checking the least significant bits
        binary_message = ''.join([str(pixel & 1) for pixel in flat_image_array])

        # Look for the message delimiter
        delimiter_index = binary_message.find('1111111111111110')
        if delimiter_index == -1:
            raise ValueError("No hidden message found in the image.")
        
        message_bits = binary_message[:delimiter_index]
        return self._decrypt_message(message_bits)

    def _load_image(self, image_path):
        """Loads an image from the given path."""
        try:
            with Image.open(image_path) as img:
                return img
        except FileNotFoundError:
            logging.error(f"Image file {image_path} not found.")
            raise
        except IOError:
            logging.error(f"Cannot open the image file {image_path}.")
            raise

    def save_key(self, key_path='secret.key', password=None):
        """
        Saves the encryption key to a file, optionally encrypting it with a password.
        """
        if password:
            aesgcm = AESGCM(self._derive_key_from_password(password))
            nonce = os.urandom(12)  # Use a unique nonce for key encryption
            encrypted_key = aesgcm.encrypt(nonce, self.key, None)
            with open(key_path, 'wb') as key_file:
                key_file.write(nonce + encrypted_key)
            logging.info(f"Encrypted key saved to {key_path}")
        else:
            with open(key_path, 'wb') as key_file:
                key_file.write(self.key)
            logging.info(f"Key saved to {key_path}")

    @staticmethod
    def load_key(key_path='secret.key', password=None, salt=None):
        """
        Loads the encryption key from a file, optionally decrypting it with a password.
        """
        try:
            with open(key_path, 'rb') as key_file:
                key_data = key_file.read()
                if password:
                    salt = salt or os.urandom(16)
                    nonce, encrypted_key = key_data[:12], key_data[12:]
                    aesgcm = AESGCM(Steganography(password=password, salt=salt).key)
                    key = aesgcm.decrypt(nonce, encrypted_key, None)
                    return key
                else:
                    return key_data
        except FileNotFoundError:
            logging.error(f"Key file {key_path} not found.")
            raise
        except IOError:
            logging.error(f"Cannot read the key file {key_path}.")
            raise

# Example usage
if __name__ == "__main__":
    password = getpass.getpass("Enter password for encryption key: ")
    steg = Steganography(password=password)
    
    # Save the key securely with password
    steg.save_key('secret.key', password=password)

    # Encode a message into the image
    steg.encode_message('input_image.png', 'Hello, this is a secret message!', 'encoded_image.png')

    # Decode the hidden message from the image
    decoded_message = steg.decode_message('encoded_image.png')
    print(f"Decoded message: {decoded_message}")