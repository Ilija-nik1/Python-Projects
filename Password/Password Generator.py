import tkinter as tk
import random
import string
import pyperclip

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
        self.length_label.grid_configure(padx=5, pady=5)
        self.length_entry.grid_configure(padx=5, pady=5)

        # Create and place generate button
        self.generate_button = tk.Button(master, text="Generate", command=self.generate_password)
        self.generate_button.grid(row=1, column=0, columnspan=2, pady=5)

        # Create and place output label
        self.password_label = tk.Label(master, text="")
        self.password_label.grid(row=2, column=0, columnspan=2, pady=5)

        # Create and place copy button
        self.copy_button = tk.Button(master, text="Copy to Clipboard", command=self.copy_password)
        self.copy_button.grid(row=3, column=0, columnspan=2, pady=5)

    def generate_password(self):
        # Get password length input
        password_length = int(self.length_entry.get())

        # Generate password
        password_characters = string.ascii_letters + string.digits + string.punctuation
        password_characters = password_characters.replace("1", "").replace("l", "").replace("0", "O")
        password = ''.join(random.choices(password_characters, k=password_length))

        # Update output label
        self.password_label.config(text=f"Generated password: {password}")

        # Store password in class variable for later use
        self.generated_password = password

    def copy_password(self):
        # Copy generated password to clipboard
        pyperclip.copy(self.generated_password)

# Create the root window and run the GUI
root = tk.Tk()
password_generator_gui = PasswordGeneratorGUI(root)
root.mainloop()