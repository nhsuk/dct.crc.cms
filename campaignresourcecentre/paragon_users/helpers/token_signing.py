from django.core.signing import TimestampSigner
from cryptography.fernet import Fernet
from django.conf import settings
import os


env = os.environ.copy()

KEY = settings.PARAGON_SIGN_KEY
SALT = settings.PARAGON_SALT
ENCRYPTION_KEY = settings.PARAGON_ENCRYPTION_KEY.encode()


def sign(token: str, sigKey=KEY, cryptKey=ENCRYPTION_KEY):
    """
    signs strings and then encrypts them
    """

    signer = TimestampSigner(key=sigKey, salt=SALT)
    token = signer.sign(token).encode()  # sign
    token = encrypt(token, key=cryptKey)  # ecrypt

    return token


def unsign(token, max_age: int, sigKey=KEY, cryptKey=ENCRYPTION_KEY):
    """
    dencrypts strings and then unsigns them
    """
    token = token.encode()
    token = decrypt(token, key=cryptKey)  # decrypt
    signer = TimestampSigner(key=sigKey, salt=SALT)
    token = token.decode()
    token = signer.unsign(value=str(token), max_age=max_age)  # unsign

    return token


def encrypt(message: bytes, key: bytes):
    return Fernet(key).encrypt(message)


def decrypt(token: bytes, key: bytes):
    return Fernet(key).decrypt(token)
