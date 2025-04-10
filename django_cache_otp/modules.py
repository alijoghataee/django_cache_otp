import base64

from cryptography.fernet import Fernet
import string
from random import choices

from django.conf import settings


def generate_random_otp(int_length: int) -> int:
    random_otp = ''.join(choices(string.digits, k=int_length))
    return int(random_otp)


def generate_key() -> bytes:
    secret_key = settings.SECRET_KEY.encode()
    key = base64.urlsafe_b64encode(secret_key[:32])
    return key


def encrypt_otp(otp) -> str:
    otp_bytes = str(otp).encode()
    fernet = Fernet(generate_key())

    encrypted_bytes = fernet.encrypt(otp_bytes)
    encrypted_otp = encrypted_bytes.decode()

    return encrypted_otp


def decrypt_otp(encrypted_otp) -> int:
    fernet = Fernet(generate_key())
    decrypted_otp = fernet.decrypt(encrypted_otp).decode()
    return int(decrypted_otp)
