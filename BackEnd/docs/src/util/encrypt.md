Module src.util.encrypt
=======================

Functions
---------

`encrypt(password: str) ‑> str`
:   Encrypts a password using the SHA-256 hashing algorithm.
    
    Args:
        password (str): The plain-text password to encrypt.
    
    Returns:
        str: The SHA-256 hash of the password in hexadecimal format, padded to 64 characters.

`generate_random_password(length=10) ‑> str`
:   Generates a secure random password containing a mix of letters, digits, and special characters.
    
    Args:
        length (int, optional): The desired length of the password. Defaults to 10.
    
    Returns:
        str: A randomly generated password.

`to_hex_string(hash_bytes: bytes) ‑> str`
:   Converts a SHA-256 hash (in bytes) into a hexadecimal string, zero-padded to 64 characters.
    
    Args:
        hash_bytes (bytes): The binary hash output to convert.
    
    Returns:
        str: A hexadecimal string representation of the hash, padded to 64 characters.