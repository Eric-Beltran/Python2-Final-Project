"""
Password hashing helpers.

The user module calls hash_password when creating accounts and checking login
attempts. Passwords are stored as SHA-256 hashes with a random salt.
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
