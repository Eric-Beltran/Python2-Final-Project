"""
When making a user will salt and hash the created password for storage
When logging in takes the input password and compares to hashed password
    • Dedicated to SHA-256 hashing.
    • Note: Passwords must start with a special character from !@#$%^&* and be
            6–12 characters long.
"""
import hashlib, os

def hash_password(password):
    salt = os.urandom(16)
    hash_pass = hashlib.sha256(salt.encode()+password.encode())

    return hash_pass.hexdigest() + ":" + salt

def check_password(password, hashed_password):
    salt = hashed_password.split(":")[1]
    hash_pass = hashlib.sha256(salt.encode()+password.encode())
    if hash_pass.hexdigest() == hashed_password:
        return True
    return False