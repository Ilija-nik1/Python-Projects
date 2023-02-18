import secrets
import string

def generate_password(length=16):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    alphabet = alphabet.replace("1", "").replace("l", "").replace("0", "O")
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    return password

password = generate_password()
print("Generated password: ", password)