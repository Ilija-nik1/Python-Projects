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

class Steganography:
    def __init__(self, key=None):
        if key:
            self.key = key.encode() if isinstance(key, str) else key
        else:
            self.key = AESGCM.generate_key(bit_length=256)
        self.nonce = os.urandom(12)  # AES-GCM nonce (12 bytes)

    def _encrypt_message(self, message):
        aesgcm = AESGCM(self.key)
        checksum = hashlib.sha256(message.encode()).digest()
        encrypted_message = aesgcm.encrypt(self.nonce, message.encode() + checksum, None)
        return ''.join([format(byte, '08b') for byte in encrypted_message])

    def _decrypt_message(self, binary_message):
        byte_array = bytearray(int(binary_message[i:i+8], 2) for i in range(0, len(binary_message), 8))
        aesgcm = AESGCM(self.key)
        decrypted_message = aesgcm.decrypt(self.nonce, bytes(byte_array), None)
        message, checksum = decrypted_message[:-32], decrypted_message[-32:]
        if hashlib.sha256(message).digest() != checksum:
            raise ValueError("Message integrity check failed.")
        return message.decode()

    def encode_message(self, image_path, message, output_image_path):
        image = self._load_image(image_path)
        image_array = np.array(image)
        
        message_binary = self._encrypt_message(message)
        message_binary += '1111111111111110'  # Delimiter to mark the end of the message
        message_length = len(message_binary)

        flat_image_array = image_array.flatten()

        if message_length > len(flat_image_array):
            raise ValueError("Message is too long to be hidden in the image.")
        
        # Randomly distribute the message bits in the image
        indices = list(range(len(flat_image_array)))
        random.shuffle(indices)
        selected_indices = indices[:message_length]

        for i, bit in zip(selected_indices, message_binary):
            flat_image_array[i] = (flat_image_array[i] & 254) | int(bit)

        # Reshape and save the new image
        encoded_image_array = flat_image_array.reshape(image_array.shape)
        encoded_image = Image.fromarray(encoded_image_array.astype('uint8'))
        encoded_image.save(output_image_path)
        print(f"Message encoded and saved to {output_image_path}")

    def decode_message(self, image_path):
        image = self._load_image(image_path)
        flat_image_array = np.array(image).flatten()

        # Extract the binary message
        binary_message = ''.join([str(pixel & 1) for pixel in flat_image_array])
        
        # Find the message by looking for the delimiter
        delimiter_index = binary_message.find('1111111111111110')
        if delimiter_index == -1:
            raise ValueError("No hidden message found in the image.")
        
        message_bits = binary_message[:delimiter_index]
        return self._decrypt_message(message_bits)

    def _load_image(self, image_path):
        try:
            with Image.open(image_path) as img:
                return img
        except FileNotFoundError:
            raise FileNotFoundError(f"Image file {image_path} not found.")
        except IOError:
            raise ValueError(f"Cannot open the image file {image_path}.")

    def save_key(self, key_path='secret.key'):
        with open(key_path, 'wb') as key_file:
            key_file.write(self.key)
        print(f"Encryption key saved to {key_path}")

    @staticmethod
    def load_key(key_path='secret.key'):
        try:
            with open(key_path, 'rb') as key_file:
                return key_file.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Key file {key_path} not found.")
        except IOError:
            raise ValueError(f"Cannot read the key file {key_path}.")

# Example usage
if __name__ == "__main__":
    # Generate or load a key
    key = Steganography.load_key('secret.key') if os.path.exists('secret.key') else AESGCM.generate_key(bit_length=256)
    steg = Steganography(key=key)

    # Save the key securely
    steg.save_key('secret.key')

    # Encode
    steg.encode_message('input_image.png', 'Hello, this is a secret message!', 'encoded_image.png')

    # Decode
    decoded_message = steg.decode_message('encoded_image.png')
    print(f"Decoded message: {decoded_message}")