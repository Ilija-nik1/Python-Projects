import tkinter as tk
import re

MIN_PASSWORD_LENGTH = 8
SPECIAL_CHARACTERS = set("!@#$%^&*()_+-=[]{};:'\"\\|,.<>?")

def check_password_strength(password):
    # Check password length
    if len(password) < MIN_PASSWORD_LENGTH:
        return "Weak: Password is too short"

    # Check for mixed case
    if not re.search(r"(?=.*[a-z])(?=.*[A-Z])", password):
        return "Weak: Password does not contain mixed case"

    # Check for digits
    if not any(char.isdigit() for char in password):
        return "Weak: Password does not contain digits"

    # Check for special characters
    if not any(char in SPECIAL_CHARACTERS for char in password):
        return "Weak: Password does not contain special characters"

    # Check for repeating characters
    if re.search(r"(.)\1{2,}", password):
        return "Weak: Password contains repeating characters"

    return "Strong"

class PasswordStrengthGUI:
    def __init__(self, master):
        self.master = master
        master.title("Password Strength Checker")

        # Configure dark mode theme
        self.configure_dark_theme()

        # Create and place password label and entry widget
        self.password_label = tk.Label(master, text="Enter password:", bg="#2b2b2b", fg="white")
        self.password_label.grid(row=0, column=0, sticky="W")
        self.password_entry = tk.Entry(master, show="*", bg="#2b2b2b", fg="white")
        self.password_entry.grid(row=0, column=1)

        # Create and place check button
        self.check_button = tk.Button(master, text="Check", command=self.check_password_strength, bg="#2b2b2b", fg="white")
        self.check_button.grid(row=1, column=0, columnspan=2)

        # Create and place output label
        self.password_strength_label = tk.Label(master, text="", bg="#2b2b2b", fg="white")
        self.password_strength_label.grid(row=2, column=0, columnspan=2)

    def configure_dark_theme(self):
        # Configure dark mode theme settings
        self.master.config(bg="#2b2b2b")
        self.master['bg'] = "#2b2b2b"
        self.master.option_add('*background', '#2b2b2b')
        self.master.option_add('*foreground', 'white')

    def check_password_strength(self):
        # Get password input
        password = self.password_entry.get()

        # Set the width of the password entry widget based on the length of the text
        width = len(password) + 1
        self.password_entry.config(width=width)

        # Check password strength
        password_strength = check_password_strength(password)

        # Update output label
        self.password_strength_label.config(text=password_strength)

# Create the root window and run the GUI
root = tk.Tk()
password_strength_gui = PasswordStrengthGUI(root)
root.mainloop()