import base64
import re

from django_otp.settings import SECRET_KEY


def _generate_totp(phone: str):
    import pyotp

    challenge = prepare_challenge(phone)
    totp = pyotp.TOTP(challenge, interval=120)
    return totp


def generate_otp_code(phone: str):
    totp = _generate_totp(phone)
    return totp.now()


def verification_otp_code(phone: str, otp: str):
    totp = _generate_totp(phone)
    return totp.verify(otp)


def prepare_challenge(phone: str) -> str:
    challenge = f'{phone}{SECRET_KEY}'
    input_bytes = challenge.encode("utf-8")
    base32_encoded = base64.b32encode(input_bytes)
    challenge = base32_encoded.decode("utf-8")
    challenge = remove_special_characters(challenge)[::-1][:40]
    return challenge


def remove_special_characters(string: str) -> str:
    return re.sub(r'[@\._=*+$-]', '', string).lower()

