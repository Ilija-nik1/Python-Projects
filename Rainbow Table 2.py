import hashlib
import bcrypt
import secrets

def create_rainbow_table(password_list):
    if not password_list:
        raise ValueError("Password list is empty")

    rainbow_table = {}
    
    # Iterate through the list of passwords
    for password in password_list:
        if not isinstance(password, str):
            raise TypeError("Password must be a string")

        # Check password strength
        if not is_strong_password(password):
            raise ValueError("Weak password: {}".format(password))
        
        # Generate a random salt
        salt = secrets.token_hex(32)
        
        # Combine the password and salt
        salted_password = password + salt
        
        # Calculate the hash of the salted password using bcrypt
        hashed_password = bcrypt.hashpw(salted_password.encode(), bcrypt.gensalt())
        
        # Add the salt, hash and the password to the rainbow table
        rainbow_table[hashed_password] = (salt, password)
        
    return rainbow_table

def is_strong_password(password):
    # Implement password strength check logic here
    return True

# Example password list
password_list = ['password1', 'password2', 'password3']

# Create the rainbow table
rainbow_table = create_rainbow_table(password_list)

print(rainbow_table)