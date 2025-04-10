from django.core.cache import cache

from django_cache_otp.modules import generate_random_otp, encrypt_otp, decrypt_otp


def generate_otp(username: str, otp_length: int = 6, timeout: int = 60) -> int:
    otp = generate_random_otp(otp_length)
    encrypted_otp = encrypt_otp(otp)
    cache.set(username, encrypted_otp, timeout=timeout)
    return otp


def validate_otp(username: str, otp: int) -> bool:
    encrypted_otp = cache.get(username)
    if not encrypted_otp:
        return False
    decrypted_otp = decrypt_otp(encrypted_otp)
    if decrypted_otp != otp:
        return False
    else:
        cache.delete(username)
        return True
