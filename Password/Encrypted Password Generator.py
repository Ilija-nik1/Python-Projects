import string
import secrets
from Crypto.Cipher import AES

class EmptyAlphabetError(Exception):
    pass

def generate_password(length=16):
    # Generate a random password
    alphabet = string.ascii_letters + string.digits + string.punctuation
    alphabet = alphabet.replace("1", "").replace("l", "").replace("0", "O")
    if not alphabet:
        raise EmptyAlphabetError("Empty alphabet after substitutions")
    password = ''.join(secrets.choice(alphabet) for i in range(length))

    # Use AES 256 encryption to encrypt the password
    key = secrets.token_bytes(32)  # 32 bytes = 256 bits
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(password.encode())
    encrypted_password = ciphertext + cipher.nonce + tag + key

    return encrypted_password.hex()

import tkinter as tk

class PasswordGeneratorGUI:
    def __init__(self, master):
        self.master = master
        master.title("Password Generator")

        # Determine maximum password length based on available window width
        max_width = master.winfo_screenwidth() // 2
        max_length = max_width // 9

        # Create and place password length label and entry widget
        self.length_label = tk.Label(master, text="Password length:")
        self.length_label.grid(row=0, column=0, sticky="W")
        self.length_entry = tk.Entry(master, width=max_length)
        self.length_entry.insert(0, "16")
        self.length_entry.grid(row=0, column=1)

        # Create and place generate button
        self.generate_button = tk.Button(master, text="Generate", command=self.generate_password)
        self.generate_button.grid(row=1, column=0, columnspan=2)

        # Create and place output label
        self.password_label = tk.Label(master, text="")
        self.password_label.grid(row=2, column=0, columnspan=2)

    def generate_password(self):
        try:
            # Get password length input
            length = int(self.length_entry.get())
        except ValueError:
            self.password_label.config(text="Invalid input: password length must be an integer")
            return

        try:
            # Generate password
            password = generate_password(length)
        except EmptyAlphabetError as e:
            self.password_label.config(text=str(e))
            return

        # Update output label
        self.password_label.config(text=f"Generated password: {password}")
        
# Create the root window and run the GUI
root = tk.Tk()
password_generator_gui = PasswordGeneratorGUI(root)
root.mainloop()