class ParagonClientError(Exception):
    pass


class PasswordError(ParagonClientError):
    pass


class ParagonClientTimeout (ParagonClientError):
    pass