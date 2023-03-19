import string
import tkinter as tk
import pyperclip

# Caesar Cipher encryption function
def encrypt(text, key):
    result = ""
    for char in text:
        if char.isalpha():
            char_index = (string.ascii_lowercase.index(char.lower()) + key) % 26
            if char.isupper():
                result += string.ascii_uppercase[char_index]
            else:
                result += string.ascii_lowercase[char_index]
        else:
            result += char
    return result

# Caesar Cipher decryption function
def decrypt(ciphertext, key):
    result = ""
    for char in ciphertext:
        if char.isalpha():
            char_index = (string.ascii_lowercase.index(char.lower()) - key) % 26
            if char.isupper():
                result += string.ascii_uppercase[char_index]
            else:
                result += string.ascii_lowercase[char_index]
        else:
            result += char
    return result

# Event handler for encrypt button
def encrypt_message():
    plaintext = plaintext_input.get()
    password = password_input.get()
    key = sum(ord(char) for char in password)
    ciphertext = encrypt(plaintext, key)
    ciphertext_display.configure(text=ciphertext)

# Event handler for decrypt button
def decrypt_message():
    ciphertext = ciphertext_display.cget("text")
    password = password_input.get()
    key = sum(ord(char) for char in password)
    plaintext = decrypt(ciphertext, key)
    plaintext_display.configure(text=plaintext)

# Event handler for copy button
def copy_text():
    if ciphertext_display.cget("text"):
        pyperclip.copy(ciphertext_display.cget("text"))
    elif plaintext_display.cget("text"):
        pyperclip.copy(plaintext_display.cget("text"))

# Create the main window
root = tk.Tk()
root.title("Caesar Cipher Encryption")

# Create the input labels and entry widgets
plaintext_label = tk.Label(root, text="Enter the message you want to encrypt:")
plaintext_input = tk.Entry(root)
password_label = tk.Label(root, text="Enter a password to use for encryption:")
password_input = tk.Entry(root, show="*")

# Create the encrypt, decrypt, and copy buttons
encrypt_button = tk.Button(root, text="Encrypt", command=encrypt_message)
decrypt_button = tk.Button(root, text="Decrypt", command=decrypt_message)
copy_button = tk.Button(root, text="Copy", command=copy_text)

# Create the output labels
ciphertext_label = tk.Label(root, text="Encrypted message:")
ciphertext_display = tk.Label(root, text="")
plaintext_label2 = tk.Label(root, text="Decrypted message:")
plaintext_display = tk.Label(root, text="")

# Pack the widgets into the window
plaintext_label.pack()
plaintext_input.pack()
password_label.pack()
password_input.pack()
encrypt_button.pack()
decrypt_button.pack()
copy_button.pack()
ciphertext_label.pack()
ciphertext_display.pack()
plaintext_label2.pack()
plaintext_display.pack()

# Start the main event loop
root.mainloop()