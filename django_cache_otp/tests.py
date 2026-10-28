from django.core.cache import cache
from django.test import TestCase

from django_cache_otp import generate_otp, validate_otp
from django_cache_otp.modules import generate_random_otp


def wrong(otp):
    return "1" + otp[1:] if otp[0] == "0" else "0" + otp[1:]


class OtpTests(TestCase):
    def setUp(self):
        cache.clear()

    def test_otp_is_string(self):
        self.assertTrue(all(len(generate_random_otp(6)) == 6 for _ in range(1000)))
        otp = generate_otp("u")
        self.assertIsInstance(otp, str)
        self.assertTrue(validate_otp("u", otp))

    def test_generate_rate_limit(self):
        self.assertIsNotNone(generate_otp("u"))
        self.assertIsNone(generate_otp("u"))
        self.assertIsNotNone(generate_otp("other"))

    def test_validate_rate_limit(self):
        otp = generate_otp("u")
        self.assertFalse(validate_otp("u", wrong(otp)))
        self.assertFalse(validate_otp("u", otp))  # too soon, not checked
        cache.delete("u:validate_rate_limit")
        self.assertTrue(validate_otp("u", otp))

    def test_invalid_after_failure(self):
        otp = generate_otp("u")
        for _ in range(3):
            self.assertFalse(validate_otp("u", wrong(otp), rate_limit=0))
        self.assertFalse(validate_otp("u", otp, rate_limit=0))  # invalidated

    def test_new_otp_resets_failures(self):
        otp = generate_otp("u")
        validate_otp("u", wrong(otp), rate_limit=0)
        validate_otp("u", wrong(otp), rate_limit=0)
        otp = generate_otp("u", rate_limit=0)
        validate_otp("u", wrong(otp), rate_limit=0)
        self.assertTrue(validate_otp("u", otp, rate_limit=0))
