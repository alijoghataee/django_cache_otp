import secrets

from django.core.cache import cache

from django_cache_otp.modules import generate_random_otp, encrypt_otp, decrypt_otp


def generate_otp(username: str, otp_length: int = 6, timeout: int = 60, skip_if_exists: bool = False,
                 rate_limit: int = 60) -> str | None:
    if skip_if_exists:
        if cache.get(username):
            return

    if rate_limit and not cache.add(f"{username}:generate_rate_limit", 1, timeout=rate_limit):
        return

    otp = generate_random_otp(otp_length)
    encrypted_otp = encrypt_otp(otp)
    cache.set(username, encrypted_otp, timeout=timeout)
    cache.set(f"{username}:failures", 0, timeout=timeout)
    return otp


def validate_otp(username: str, otp: str, rate_limit: int = 5, invalid_after_failure: int = 3) -> bool:
    if rate_limit and not cache.add(f"{username}:validate_rate_limit", 1, timeout=rate_limit):
        return False

    encrypted_otp = cache.get(username)
    if not encrypted_otp:
        return False
    decrypted_otp = decrypt_otp(encrypted_otp)
    if not secrets.compare_digest(decrypted_otp, str(otp)):
        if invalid_after_failure:
            failures_key = f"{username}:failures"
            cache.add(failures_key, 0)
            if cache.incr(failures_key) >= invalid_after_failure:
                cache.delete_many([username, failures_key])
        return False
    else:
        cache.delete_many([username, f"{username}:failures"])
        return True
