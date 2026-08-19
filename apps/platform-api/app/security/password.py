"""
Password hashing utilities.

Passwords must never be stored in plaintext.

This module uses Argon2id through argon2-cffi to:
    - hash passwords before persistence
    - verify plaintext passwords during authentication

The resulting password hash is safe to store in the database.
"""

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

_password_hasher = PasswordHasher()

def hash_password(password: str) -> str:
    """
    Hash a plaintext password using Argon2id.
    """
    return _password_hasher.hash(password)

def verify_password(password: str, password_hash: str) -> bool:
    """
    Verify a plaintext password against an Argon2 hash.
    """
    try:
        return _password_hasher.verify(password_hash, password)
    except VerifyMismatchError:
        return False