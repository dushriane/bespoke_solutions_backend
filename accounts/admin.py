from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from accounts.models import (
    User,
    VerificationCode,
    Designer,
    ExternalPartner,
    Address,
    TaxInformation,
    UserSettings,
)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("id", "email", "full_name", "phone_number", "user_type", "is_staff", "is_active", "created_at")
    search_fields = ("email", "full_name", "phone_number")
    list_filter = ("user_type", "is_staff", "is_active", "is_first_login", "created_at")
    ordering = ("-created_at",)
    sortable_by = ("id", "email", "full_name", "phone_number", "user_type", "is_staff", "is_active", "created_at")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("full_name", "phone_number", "address")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_admin", "is_superuser", "user_type", "is_customer", "is_partners", "is_first_login")}),
        ("Important dates", {"fields": ("last_login", "created_at")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "full_name", "phone_number", "address", "password1", "password2", "is_staff", "is_active"),
        }),
    )


@admin.register(VerificationCode)
class VerificationCodeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "code", "purpose", "is_verified", "created_at", "expires_at")
    search_fields = ("user__email", "user__full_name", "code")
    list_filter = ("purpose", "is_verified", "created_at", "expires_at")
    ordering = ("-created_at",)
    sortable_by = ("id", "user", "code", "purpose", "is_verified", "created_at", "expires_at")


@admin.register(Designer)
class DesignerAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "specialization", "experience_level", "availability_status", "created_at")
    search_fields = ("user__email", "user__full_name", "specialization", "experience_level")
    list_filter = ("availability_status", "created_at")
    ordering = ("-created_at",)
    sortable_by = ("id", "user", "specialization", "experience_level", "availability_status", "created_at")


@admin.register(ExternalPartner)
class ExternalPartnerAdmin(admin.ModelAdmin):
    list_display = ("id", "company_name", "partner_type", "user", "contact_email", "is_active", "created_at")
    search_fields = ("company_name", "partner_type", "contact_email", "user__email")
    list_filter = ("partner_type", "is_active", "created_at")
    ordering = ("-created_at",)
    sortable_by = ("id", "company_name", "partner_type", "user", "contact_email", "is_active", "created_at")


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "street", "district", "country", "is_default", "created_at")
    search_fields = ("user__email", "user__full_name", "street", "district", "country")
    list_filter = ("is_default", "country", "created_at")
    ordering = ("-created_at",)
    sortable_by = ("id", "user", "street", "district", "country", "is_default", "created_at")


@admin.register(TaxInformation)
class TaxInformationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "tin_number", "business_name", "tax_type", "created_at")
    search_fields = ("tin_number", "business_name", "tax_type", "user__email")
    list_filter = ("tax_type", "created_at")
    ordering = ("-created_at",)
    sortable_by = ("id", "user", "tin_number", "business_name", "tax_type", "created_at")


@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "language", "notifications_enabled", "dark_mode", "created_at")
    search_fields = ("user__email", "user__full_name", "language")
    list_filter = ("notifications_enabled", "dark_mode", "language", "created_at")
    ordering = ("-created_at",)
    sortable_by = ("id", "user", "language", "notifications_enabled", "dark_mode", "created_at")