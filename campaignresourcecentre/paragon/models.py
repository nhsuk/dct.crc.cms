from django.db import models


class ParagonCacheValues(models.Model):
    """
    Model to store single row containing cached Paragon values
    """

    num_users = models.IntegerField(default=0)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
