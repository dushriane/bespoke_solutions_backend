from django.contrib import admin
from product.models import Product, ProductCategory, ProductVariant
admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(ProductVariant)