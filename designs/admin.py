from django.contrib import admin
from designs.models import Design

@admin.register(Design)
class DesignAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "status", "created_at")
    search_fields = ("name", "status")
    list_filter = ("status", "created_at")
    ordering = ("-created_at",)
    sortable_by = ("name", "status", "created_at")