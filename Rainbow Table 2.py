import hashlib
import secrets

def create_rainbow_table(password_list):
    rainbow_table = {}
    
    # Iterate through the list of passwords
    for password in password_list:
        # Generate a random salt
        salt = secrets.token_hex(16)
        
        # Combine the password and salt
        salted_password = password + salt
        
        # Calculate the hash of the salted password using SHA256
        hashed_password = hashlib.sha256(salted_password.encode()).hexdigest()
        
        # Add the salt, hash and the password to the rainbow table
        rainbow_table[hashed_password] = (salt, password)
        
    return rainbow_table

# Example password list
password_list = ['password1', 'password2', 'password3']

# Create the rainbow table
rainbow_table = create_rainbow_table(password_list)

print(rainbow_table)