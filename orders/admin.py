from django.contrib import admin
from orders.models import *
admin.site.register(Order)
admin.site.register(Shipment)
admin.site.register(Payment)
admin.site.register(OrderItem)
admin.site.register(ShipmentStatusHistory)
admin.site.register(ShipmentStatus)