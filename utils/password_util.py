import hashlib

import bcrypt


def is_valid_password(password: str, hashed_password: bytes, salt: bytes) -> bool:
    return get_hashed_password(password, salt) == hashed_password


def generate_salt() -> bytes:
    new_salt = bcrypt.gensalt(rounds=5)
    return new_salt


def get_hashed_password(password: str, salt: bytes) -> bytes:
    hashed_password = hashlib.sha512(password.encode() + salt).digest()
    return hashed_password
