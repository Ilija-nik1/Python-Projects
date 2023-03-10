import hashlib

def create_rainbow_table(password_list):
    rainbow_table = {}
    
    # Iterate through the list of passwords
    for password in password_list:
        # Calculate the hash of the password
        hashed_password = hashlib.sha1(password.encode()).hexdigest()
        
        # Add the hash and the password to the rainbow table
        rainbow_table[hashed_password] = password
        
    return rainbow_table

# Example password list
password_list = ['password1', 'password2', 'password3']

# Create the rainbow table
rainbow_table = create_rainbow_table(password_list)

print(rainbow_table)