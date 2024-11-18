import hashlib
import uuid


def sha256(password: str) -> str:
    salt = uuid.uuid4().hex
    enc = hashlib.sha256()
    enc.update(salt.encode())
    enc.update(password.encode())
    enc.digest()
    return enc.hexdigest()
