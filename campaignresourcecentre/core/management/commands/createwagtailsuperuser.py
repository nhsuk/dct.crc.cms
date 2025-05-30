from os import environ

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        wagtail_user = environ.get("WAGTAIL_USER")
        if wagtail_user:
            wagtail_password = environ.get("WAGTAIL_PASSWORD")
            if wagtail_password:
                user_model = get_user_model()
                try:
                    superuser = user_model.objects.get(username=wagtail_user)
                    superuser.set_password(wagtail_password)
                    self.stdout.write("Superuser '%s' updated" % wagtail_user)
                except user_model.DoesNotExist:
                    superuser = user_model.objects.create_superuser(
                        username=wagtail_user,
                        email="noone@example.com",
                        password=wagtail_password,
                        is_staff=True,
                    )
                    self.stdout.write("Superuser '%s' created" % wagtail_user)
                superuser.save()
            else:
                self.stdout.write(
                    "No WAGTAIL_PASSWORD symbol in environment - no superuser created"
                )
        else:
            self.stdout.write(
                "No WAGTAIL_USER symbol in environment - no superuser created"
            )
