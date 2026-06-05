from django.contrib import admin
from designs.models import Design

@admin.register(Design)
class DesignAdmin(admin.ModelAdmin):
    list_display = ("id", "design_name", "file_name", "file_type", "uploaded_by", "created_at")
    search_fields = ("design_name", "file_name", "file_type", "uploaded_by__email")
    list_filter = ("file_type", "created_at", "updated_at")
    ordering = ("-created_at",)
    sortable_by = ("design_name", "file_name", "file_type", "created_at", "updated_at")