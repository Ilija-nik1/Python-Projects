from PIL import Image
import numpy as np
from cryptography.fernet import Fernet
import os

class Steganography:
    def __init__(self, key=None):
        if key:
            self.key = key.encode() if isinstance(key, str) else key
        else:
            self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)

    def _encrypt_message(self, message):
        encrypted_message = self.cipher.encrypt(message.encode())
        return ''.join([format(byte, '08b') for byte in encrypted_message])
    
    def _decrypt_message(self, binary_message):
        byte_array = bytearray(int(binary_message[i:i+8], 2) for i in range(0, len(binary_message), 8))
        encrypted_message = bytes(byte_array)
        return self.cipher.decrypt(encrypted_message).decode()

    def encode_message(self, image_path, message, output_image_path):
        image = self._load_image(image_path)
        image_array = np.array(image)
        
        message_binary = self._encrypt_message(message)
        message_binary += '1111111111111110'  # Delimiter to mark the end of the message
        message_length = len(message_binary)

        flat_image_array = image_array.flatten()

        if message_length > len(flat_image_array):
            raise ValueError("Message is too long to be hidden in the image.")
        
        # Encode the message into the image
        flat_image_array[:message_length] = [
            (pixel & 254) | int(bit)
            for pixel, bit in zip(flat_image_array[:message_length], message_binary)
        ]

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
    key = Steganography.load_key('secret.key') if os.path.exists('secret.key') else Fernet.generate_key()
    steg = Steganography(key=key)

    # Save the key securely
    steg.save_key('secret.key')

    # Encode
    steg.encode_message('input_image.png', 'Hello, this is a secret message!', 'encoded_image.png')

    # Decode
    decoded_message = steg.decode_message('encoded_image.png')
    print(f"Decoded message: {decoded_message}")