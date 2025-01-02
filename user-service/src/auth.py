from argon2 import PasswordHasher

ph = PasswordHasher()

def hash_pass(password: str):
    hashed_password = ph.hash(password)
    return hashed_password

def verify_pass(password: str, hashed_password: str):
    try:
        return ph.verify(hashed_password, password)
    except Exception:
        return False