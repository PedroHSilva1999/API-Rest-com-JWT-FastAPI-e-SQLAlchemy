from passlib.context import CryptContext

CRIPTO = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_password_hash(password: str) -> str:
    return CRIPTO.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return CRIPTO.verify(password, hashed_password)

