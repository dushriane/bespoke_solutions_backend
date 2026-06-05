from django.contrib import admin
from customization.models import Customization, DesignPlacement, DesignerAssignment


@admin.register(Customization)
class CustomizationAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "product", "variant", "design", "status", "created_at")
    search_fields = ("customer__email", "product__product_name", "variant__sku", "design_name", "custom_text")
    list_filter = ("status", "created_at", "product", "design")
    ordering = ("-created_at",)
    sortable_by = ("id", "customer", "product", "variant", "design", "status", "created_at")


@admin.register(DesignPlacement)
class DesignPlacementAdmin(admin.ModelAdmin):
    list_display = ("id", "customization", "side_position", "layer_order", "created_at")
    search_fields = ("customization__id", "side_position")
    list_filter = ("side_position", "created_at")
    ordering = ("-created_at",)
    sortable_by = ("id", "customization", "side_position", "layer_order", "created_at")


@admin.register(DesignerAssignment)
class DesignerAssignmentAdmin(admin.ModelAdmin):
    list_display = ("id", "customization", "order_item", "designer", "assigned_by", "status", "deadline", "created_at")
    search_fields = ("customization__id", "designer__email", "assigned_by__email", "remarks")
    list_filter = ("status", "assigned_at", "deadline", "created_at")
    ordering = ("-created_at",)
    sortable_by = ("id", "customization", "order_item", "designer", "assigned_by", "status", "deadline", "created_at")