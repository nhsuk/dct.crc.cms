from re import search, compile as rcompile
from django.core.exceptions import ValidationError
from campaignresourcecentre.paragon.exceptions import PasswordError
from django.utils.translation import gettext_lazy


regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&£_<>~^.+=|-])[A-Za-z\d@$!%*#?&£_<>~^.+=|-]{8,128}$"  # noqa
error = "Password must be at least 9 characters long, and contain at least 1 number, 1 capital letter, 1 lowercase letter and 1 symbol"


def validate_password_form(password):
    pattern = rcompile(regex)
    matching = search(pattern, password)
    if matching is None:
        raise ValidationError(gettext_lazy(error))


def validate_password_data_classes(password):
    pattern = rcompile(regex)
    matching = search(pattern, password)
    if matching:
        return True
    else:
        raise PasswordError(error)
