from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv
load_dotenv()

FERNET_KEY = os.getenv("FERNET_KEY", None)
if not FERNET_KEY:
    FERNET_KEY = Fernet.generate_key().decode()
fernet = Fernet(FERNET_KEY.encode())

def encrypt_token(token: str) -> str:
    return fernet.encrypt(token.encode()).decode()

def decrypt_token(token_enc: str) -> str:
    return fernet.decrypt(token_enc.encode()).decode()
