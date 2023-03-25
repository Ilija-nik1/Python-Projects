import string
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.simpledialog
import tkinter.filedialog
import pyperclip
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# AES encryption function
def encrypt(text, key):
    key = key.encode("utf-8")  # Convert password to bytes
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext, iv = cipher.encrypt_and_digest(pad(text.encode("utf-8"), AES.block_size))
    return iv + ciphertext

# AES decryption function
def decrypt(ciphertext, key):
    key = key.encode("utf-8")  # Convert password to bytes
    iv = ciphertext[:AES.block_size]
    ciphertext = ciphertext[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext.decode("utf-8")

# Event handler for encrypt button
def encrypt_message():
    plaintext = plaintext_input.get()
    password = tkinter.simpledialog.askstring("Password", "Enter a password to use for encryption:", show='*')
    if password:
        ciphertext = encrypt(plaintext, password)
        ciphertext_display.configure(text=ciphertext.hex())

# Event handler for decrypt button
def decrypt_message():
    ciphertext_hex = ciphertext_display.cget("text")
    password = tkinter.simpledialog.askstring("Password", "Enter the password used for encryption:", show='*')
    if password:
        if ciphertext_hex:
            try:
                ciphertext = bytes.fromhex(ciphertext_hex)
                plaintext = decrypt(ciphertext, password)
                plaintext_display.configure(text=plaintext)
            except ValueError:
                tk.messagebox.showerror("Error", "Invalid ciphertext")

# Event handler for copy button
def copy_text():
    text = ciphertext_display.cget("text") or plaintext_display.cget("text")
    if text:
        pyperclip.copy(text)

# Event handler for encrypt file button
def encrypt_file():
    password = tkinter.simpledialog.askstring("Password", "Enter a password to use for encryption:", show='*')
    if password:
        filepath = tkinter.filedialog.askopenfilename()
        if filepath:
            with open(filepath, 'rb') as f:
                plaintext = f.read()
            ciphertext = encrypt(plaintext, password)
            with open(filepath + '.enc', 'wb') as f:
                f.write(ciphertext)

# Event handler for decrypt file button
def decrypt_file():
    password = tkinter.simpledialog.askstring("Password", "Enter the password used for encryption:", show='*')
    if password:
        filepath = tkinter.filedialog.askopenfilename()
        if filepath:
            with open(filepath, 'rb') as f:
                ciphertext = f.read()
            try:
                plaintext = decrypt(ciphertext, password)
                with open(filepath[:-4], 'wb') as f:
                    f.write(plaintext)
            except ValueError:
                tk.messagebox.showerror("Error", "Invalid ciphertext")

# Create the main window
root = tk.Tk()
root.title("AES Encryption")

# Create the input labels and entry widgets
plaintext_label = ttk.Label(root, text="Enter the message you want to encrypt:")
plaintext_input = ttk.Entry(root)
password_label = ttk.Label(root, text="Enter a password to use for encryption:")
password_input = ttk.Entry(root, show="*")

# Create the encrypt, decrypt, and copy buttons
encrypt_button = ttk.Button(root, text="Encrypt", command=encrypt_message)
decrypt_button = ttk.Button(root, text="Decrypt", command=decrypt_message)
copy_button = ttk.Button(root, text="Copy", command=copy_text)

#Create the ciphertext and plaintext display labels
ciphertext_label = ttk.Label(root, text="Ciphertext:")
ciphertext_display = ttk.Label(root, wraplength=400)
plaintext_label2 = ttk.Label(root, text="Plaintext:")
plaintext_display = ttk.Label(root, wraplength=400)

#Create the file encryption and decryption buttons
encrypt_file_button = ttk.Button(root, text="Encrypt File", command=encrypt_file)
decrypt_file_button = ttk.Button(root, text="Decrypt File", command=decrypt_file)

#Set the layout using the grid geometry manager
plaintext_label.grid(column=0, row=0, padx=5, pady=5, sticky="w")
plaintext_input.grid(column=0, row=1, padx=5, pady=5, sticky="ew")
password_label.grid(column=0, row=2, padx=5, pady=5, sticky="w")
password_input.grid(column=0, row=3, padx=5, pady=5, sticky="ew")
encrypt_button.grid(column=0, row=4, padx=5, pady=5)
decrypt_button.grid(column=0, row=5, padx=5, pady=5)
copy_button.grid(column=0, row=6, padx=5, pady=5)
ciphertext_label.grid(column=0, row=7, padx=5, pady=5, sticky="w")
ciphertext_display.grid(column=0, row=8, padx=5, pady=5, sticky="ew")
plaintext_label2.grid(column=0, row=9, padx=5, pady=5, sticky="w")
plaintext_display.grid(column=0, row=10, padx=5, pady=5, sticky="ew")
encrypt_file_button.grid(column=0, row=11, padx=5, pady=5)
decrypt_file_button.grid(column=0, row=12, padx=5, pady=5)

#Set the window size and disable resizing
root.geometry("500x600")
root.resizable(False, False)

#Start the main event loop
root.mainloop()