import re

def check_password_strength(password):
    # Check password length
    if len(password) < 8:
        return "Weak: Password is too short"

    # Check for mixed case
    if not any(char.isupper() for char in password) or not any(char.islower() for char in password):
        return "Weak: Password does not contain mixed case"

    # Check for digits
    if not any(char.isdigit() for char in password):
        return "Weak: Password does not contain digits"

    # Check for special characters
    if not any(char in set("!@#$%^&*()_+-=[]{};:'\"\\|,.<>?") for char in password):
        return "Weak: Password does not contain special characters"

    # Check for common passwords
    with open("common_passwords.txt", "r") as f:
        common_passwords = f.readlines()
    common_passwords = [x.strip() for x in common_passwords]
    if password in common_passwords:
        return "Weak: Password is a common password"

    # Check for repeating characters
    if re.search(r'(.)\1{2,}', password):
        return "Weak: Password contains repeating characters"

    return "Strong"

password = input("Enter password: ")
password_strength = check_password_strength(password)
print(password_strength)