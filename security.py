"""
When making a user will salt and hash the created password for storage.
When logging in takes the input password and compares to hashed password.
"""

import hashlib
import os


def hash_password(password, salt=None):
    """
    Hash a password with SHA-256 and a salt.

    Returns:
    - hashed password
    - salt as a hex string
    """

    if salt is None:
        salt = os.urandom(16)

    if isinstance(salt, str):
        salt = bytes.fromhex(salt)

    hashed_password = hashlib.sha256(salt + password.encode()).hexdigest()

    return hashed_password, salt.hex()