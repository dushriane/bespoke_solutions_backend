from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Order(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


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
    status = models.CharField(max_length=50)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Status {self.status} for Shipment {self.shipment.id} at {self.updated_at}"
    
    