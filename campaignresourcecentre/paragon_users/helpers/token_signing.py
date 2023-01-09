from base64 import b64encode
from django.core.signing import TimestampSigner
from cryptography.fernet import Fernet
from django.conf import settings
import os
import logging


logger = logging.getLogger(__name__)
env = os.environ.copy()

KEY = settings.PARAGON_SIGN_KEY
SALT = settings.PARAGON_SALT
PARAGON_ENCRYPTION_KEY = settings.PARAGON_ENCRYPTION_KEY or "Default Value"
if PARAGON_ENCRYPTION_KEY == "Default Value":
    logger.warning("Paragon Encryption Key Not Set")
    # Key must be base 64 encoding of a 32 byte value
    # We use the encoding of 'DEFAULTVALUE34567890123456789012' as default for testing
    PARAGON_ENCRYPTION_KEY = b64encode(b"DEFAULTVALUE34567890123456789012")
ENCRYPTION_KEY = PARAGON_ENCRYPTION_KEY


def sign(token: str, sig_key=KEY, cryptKey=ENCRYPTION_KEY):
    """
    signs strings and then encrypts them
    """

    signer = TimestampSigner(key=sig_key, salt=SALT)
    token = signer.sign(token).encode()  # sign
    token = encrypt(token, key=cryptKey)  # ecrypt

    return token


def unsign(token, max_age=None, sig_key=KEY, cryptKey=ENCRYPTION_KEY):
    """
    dencrypts strings and then unsigns them
    """
    token = token.encode()
    token = decrypt(token, key=cryptKey)  # decrypt
    signer = TimestampSigner(key=sig_key, salt=SALT)
    token = token.decode()
    token = signer.unsign(value=str(token), max_age=max_age)  # unsign

    return token


def encrypt(message: bytes, key: bytes):
    return Fernet(key).encrypt(message)


def decrypt(token: bytes, key: bytes):
    return Fernet(key).decrypt(token)
