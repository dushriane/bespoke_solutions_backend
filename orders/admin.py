from django.contrib import admin
from orders.models import Order, OrderItem, Payment, Shipment, ShipmentStatusHistory


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "subtotal",
        "tax_amount",
        "delivery_fee",
        "total_amount",
        "order_status",
        "payment_status",
        "placed_at",
    )
    list_filter = ("order_status", "payment_status", "placed_at")
    search_fields = ("id", "user__email", "user__full_name")
    readonly_fields = ("id", "placed_at", "created_at", "updated_at")
    autocomplete_fields = ("user", "cart", "address", "tax_information", "partner")


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "product_name", "quantity", "price")
    search_fields = ("product_name", "order__name")
    list_filter = ("order",)
    ordering = ("order",)
    sortable_by = ("id", "order", "product_name", "quantity", "price")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "amount", "payment_method", "payment_date")
    search_fields = ("order__name", "payment_method")
    list_filter = ("payment_method", "payment_date")
    ordering = ("-payment_date",)
    sortable_by = ("id", "order", "amount", "payment_method", "payment_date")


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "tracking_number", "carrier", "shipment_date")
    search_fields = ("tracking_number", "carrier", "order__name")
    list_filter = ("carrier", "shipment_date")
    ordering = ("-shipment_date",)
    sortable_by = ("id", "order", "tracking_number", "carrier", "shipment_date")


@admin.register(ShipmentStatusHistory)
class ShipmentStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "shipment", "status", "updated_at")
    search_fields = ("shipment__tracking_number", "status")
    list_filter = ("status", "updated_at")
    ordering = ("-updated_at",)
    sortable_by = ("id", "shipment", "status", "updated_at")