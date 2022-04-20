from django.db.models import CharField, Model

# Dummy model to allow Paragon user management permissions
# to be added
class ParagonUserAdmin(Model):
    class Meta:
        default_permissions = []  # don't create the default add / change / delete / view perms
        permissions = [
            ('manage_paragon_users', "Can view CRC users and change access level"),
            ('manage_paragon_users_all_fields', "Can view CRC users and change all details"),
        ]


class VerificationEmail(Model):
    user_token = CharField(max_length=256)
    email = CharField(max_length=256)
    url = CharField(max_length=256)
    first_name = CharField(max_length=256)


class PasswordResetEmail(Model):
    user_token = CharField(max_length=256)
    email = CharField(max_length=256)
    url = CharField(max_length=256)
