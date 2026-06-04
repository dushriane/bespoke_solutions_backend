from django.contrib import admin
from cart.models import Cart, CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "cart_id", "created_at", "updated_at")
    search_fields = ("cart_id",)
    list_filter = ("created_at", "updated_at")
    ordering = ("-created_at",)
    sortable_by = ("id", "cart_id", "created_at", "updated_at")


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("id", "cart", "product_name", "quantity", "price")
    search_fields = ("product_name", "cart__cart_id")
    list_filter = ("cart",)
    ordering = ("cart",)
    sortable_by = ("id", "cart", "product_name", "quantity", "price")