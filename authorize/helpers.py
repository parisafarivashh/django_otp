import base64
import re

import pyotp

from django_otp.settings import SECRET_KEY


def generate_otp_code(phone: str):
    challenge = prepare_challenge(phone)
    totp = pyotp.TOTP(challenge, interval=120)
    return totp.now()


def verification_otp_code(phone: str, otp: str):
    challenge = prepare_challenge(phone)
    totp = pyotp.TOTP(challenge, interval=120)
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

