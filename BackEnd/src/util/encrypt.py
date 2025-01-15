import hashlib
import random
import string


def encrypt(password: str) -> str:
    """
    Encrypts a password using the SHA-256 hashing algorithm.

    Args:
        password (str): The plain-text password to encrypt.

    Returns:
        str: The SHA-256 hash of the password in hexadecimal format, padded to 64 characters.
    """
    sha256 = hashlib.sha256()
    sha256.update(password.encode('utf-8'))
    return to_hex_string(sha256.digest())


def to_hex_string(hash_bytes: bytes) -> str:
    """
    Converts a SHA-256 hash (in bytes) into a hexadecimal string, zero-padded to 64 characters.

    Args:
        hash_bytes (bytes): The binary hash output to convert.

    Returns:
        str: A hexadecimal string representation of the hash, padded to 64 characters.
    """
    hex_string = hash_bytes.hex()
    return hex_string.zfill(64)


def generate_random_password(length=10) -> str:
    """
    Generates a secure random password containing a mix of letters, digits, and special characters.

    Args:
        length (int, optional): The desired length of the password. Defaults to 10.

    Returns:
        str: A randomly generated password.
    """
    all_characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(all_characters) for _ in range(length))
    return password
