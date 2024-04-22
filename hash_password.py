import hashlib

def hash_password(pwd):
    """using SHA-256 algorithm"""
    pwd_bytes = pwd.encode('utf-8')
    hashed_pwd = hashlib.sha256(pwd_bytes).hexdigest()
    return hashed_pwd