from django.contrib import admin
from product.models import Product, ProductCategory, ProductVariant


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "parent_category", "is_active", "created_at")
    search_fields = ("name", "description")
    list_filter = ("is_active", "created_at")
    ordering = ("name",)
    sortable_by = ("id", "name", "parent_category", "is_active", "created_at")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "product_name", "category", "base_price", "product_type", "is_active", "created_at")
    search_fields = ("product_name", "description", "category__name", "product_type")
    list_filter = ("is_active", "product_type", "category", "created_at")
    ordering = ("-created_at",)
    sortable_by = ("id", "product_name", "category", "base_price", "product_type", "is_active", "created_at")


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "sku", "fabric_type", "color", "size", "material", "stock_quantity", "price_delta", "is_active", "created_at")
    search_fields = ("sku", "product__product_name", "fabric_type", "color", "size", "material")
    list_filter = ("is_active", "fabric_type", "color", "size", "material", "created_at")
    ordering = ("-created_at",)
    sortable_by = ("id", "product", "sku", "stock_quantity", "price_delta", "is_active", "created_at")