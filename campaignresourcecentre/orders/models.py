from django.db import models


class OrderSequenceNumber(models.Model):
    date = models.DateField()
    seq_number = models.IntegerField()
    order_number = models.CharField(max_length=30)

    class Meta:
        unique_together = ("date", "seq_number")
