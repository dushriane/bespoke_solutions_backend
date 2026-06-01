from django.db import models
from accounts.models import User
from product.models import Product, ProductVariant
from designs.models import Design

# Create your models here.
class Customization(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True, blank=True)
    design = models.ForeignKey(Design, on_delete=models.SET_NULL, null=True, blank=True)

    design_name = models.CharField(max_length=255, null=True, blank=True)
    placement = models.CharField(max_length=100, null=True, blank=True)
    custom_text = models.TextField(null=True, blank=True)
    design_notes = models.TextField(null=True, blank=True)
    preview_3d_config = models.JSONField(null=True, blank=True)

    status = models.CharField(max_length=50, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Customization {self.id} for {self.product.product_name}"

class DesignPlacement(models.Model):
    customization = models.ForeignKey(Customization, on_delete=models.CASCADE)
    side_position = models.CharField(max_length=100, null=True, blank=True)
    x_coordinate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    y_coordinate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    width = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    height = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    rotation = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    opacity = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    layer_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Placement for {self.customization.id}"

class DesignerAssignment(models.Model):
    customization = models.ForeignKey(Customization, on_delete=models.CASCADE)
    order_item = models.ForeignKey('orders.OrderItem', on_delete=models.CASCADE, null=True, blank=True) #change here
    designer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='designer_assignments')
    assigned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assignments_given')

    assigned_at = models.DateTimeField(null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    status = models.CharField(max_length=50, null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Assignment {self.id} for {self.customization.id}"