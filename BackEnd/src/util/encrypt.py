import hashlib


def encrypt(password: str) -> str:
    sha256 = hashlib.sha256()
    sha256.update(password.encode('utf-8'))
    return to_hex_string(sha256.digest())


def to_hex_string(hash_bytes: bytes) -> str:
    hex_string = hash_bytes.hex()
    return hex_string.zfill(64)