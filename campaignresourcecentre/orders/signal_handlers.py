from django.dispatch import receiver
from django.db.models.signals import pre_save

from campaignresourcecentre.orders.models import OrderSequenceNumber


@receiver(pre_save, sender=OrderSequenceNumber)
def update_order_number(sender, instance, **kwargs):
    order_number = f'CRC3{instance.date.strftime("%y%m%d")}{instance.seq_number}'
    instance.order_number = order_number
