from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import User, Address, TaxInformation, ExternalPartner
from cart.models import Cart


# Create your models here.

class ShipmentStatus(models.TextChoices):
    CREATED = 'CREATED', _('Created')
    PICKED_UP = 'PICKED_UP', _('Picked Up')
    IN_TRANSIT = 'IN_TRANSIT', _('In Transit')
    OUT_FOR_DELIVERY = 'OUT_FOR_DELIVERY', _('Out For Delivery')
    DELIVERED = 'DELIVERED', _('Delivered')
    RETURNED = 'RETURNED', _('Returned')
    CANCELLED = 'CANCELLED', _('Cancelled')


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    tax_information = models.ForeignKey(TaxInformation, on_delete=models.SET_NULL, null=True, blank=True)
    partner = models.ForeignKey(ExternalPartner, on_delete=models.SET_NULL, null=True, blank=True)

    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    order_status = models.CharField(max_length=50, default='pending')
    payment_status = models.CharField(max_length=50, default='unpaid')

    placed_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.total_amount


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product_name} @ {self.price}"


class Payment(models.Model):
    order = models.ForeignKey(Order, related_name='payments', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment of {self.amount} for Order {self.order.id}"
    

class Shipment(models.Model):
    order = models.ForeignKey(Order, related_name='shipments', on_delete=models.CASCADE)
    shipment_date = models.DateTimeField(auto_now_add=True)
    tracking_number = models.CharField(max_length=255)
    carrier = models.CharField(max_length=255)

    def __str__(self):
        return f"Shipment for Order {self.order.id} with tracking number {self.tracking_number}"

    

class ShipmentStatusHistory(models.Model):
    shipment = models.ForeignKey(Shipment, related_name='status_history', on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=ShipmentStatus.choices, default=ShipmentStatus.CREATED)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Status {self.status} for Shipment {self.shipment.id} at {self.updated_at}"
    
    