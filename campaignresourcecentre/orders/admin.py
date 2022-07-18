from django.contrib import admin

from .models import OrderSequenceNumber


class OrderSequenceNumberAdmin(admin.ModelAdmin):
    readonly = "order_number"
    list_display = ("date", "seq_number", "order_number")


admin.site.register(OrderSequenceNumber, OrderSequenceNumberAdmin)
