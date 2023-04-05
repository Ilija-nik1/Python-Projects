import hashlib
import secrets

# The characters to use for the password
chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"
chars_len = len(chars)

# Reduces an integer i to a password of length pwd_len
def reduce(i, pwd_len):
    if not isinstance(i, int) or i < 0:
        raise ValueError("Input must be a non-negative integer")
        
    pwd = ""
    # Use a for loop instead of a while loop to generate the password
    for _ in range(pwd_len):
        pwd += chars[i % chars_len]
        i //= chars_len
    return pwd

# Generate a table of password chains
table = []
for s in range(1000):
    # Use reduce to generate the start of a chain
    start = reduce(s, 8)
    p = start
    for i in range(1000):
        # Hash the password using a secure hashing algorithm
        h = hashlib.sha256(p.encode('ascii')).hexdigest()
        # Reduce the hash to a new password
        p = reduce(int(h, 16), 8)
    table.append([start, p])

# Print the table of password chains
for start, end in table:
    print(f"{start}: {end}")