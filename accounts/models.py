from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.translation import gettext_lazy as _


class UserManager (BaseUserManager):
    def create_user(self, email, full_name, phone_number, password=None,address="", role=None, **extra_fields):
        user = self.model(
            email=email,
            full_name=full_name,
            phone_number=phone_number,
            address=address,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, full_name, phone_number, password=None, **extra_fields):
        user = self.create_user(
            email=email,
            full_name=full_name,
            phone_number=phone_number,
            password=password,
            **extra_fields
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True 
        user.save(using=self._db)
        return user
    
class User(AbstractBaseUser,PermissionsMixin):
    USER='USER'
    ADMIN='ADMIN'
    BESPOKETEAM='BESPOKETEAM'
    PARTNERS='PARTNERS'
    CUSTOMER='CUSTOMER'
    USER_TYPE_CHOICES = [
        (USER, 'User'),
        (ADMIN, 'Admin'),
        (BESPOKETEAM, 'Bespoke Team'),
        (PARTNERS, 'Partners'),
        (CUSTOMER, 'Customer')
    ]

    full_name = models.CharField(_("full name"), max_length=100)
    email = models.EmailField(_("email address"), unique=True)
    phone_number = models.CharField(_("phone number"), max_length=13, unique=True, validators=[MinLengthValidator(10), MaxLengthValidator(13)])
    address = models.TextField(_("address"), blank=True)

    is_active = models.BooleanField(_("is active"), default=True)
    user_type = models.CharField(_("user type"), max_length=20, choices=USER_TYPE_CHOICES, default=USER)

                                                                                                                                                                                                        
    is_admin = models.BooleanField(_("is admin"), default=False)
    is_staff = models.BooleanField(_("is staff"), default=False)
    is_customer = models.BooleanField(_("is customer"), default=False)
    is_partners = models.BooleanField(_("is partners"), default=False)
    is_first_login = models.BooleanField(_("is first login"), default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'phone_number']

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
class VerificationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="verification_codes")
    code = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.code
    


# class for designer
class DesignerAvailability(models.TextChoices):
    AVAILABLE = 'AVAILABLE', _('Available')
    BUSY = 'BUSY', _('Busy')
    OFFLINE = 'OFFLINE', _('Offline')
    UNKNOWN = 'UNKNOWN', _('Unknown')


# class for designer
class Designer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='designer_profile')
    specialization = models.CharField(max_length=255)
    experience_level = models.CharField(max_length=50)
    availability_status = models.CharField(max_length=50, choices=DesignerAvailability.choices, default=DesignerAvailability.UNKNOWN)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.full_name} - {self.specialization}"

# class for external_partner
class ExternalPartner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='external_partners')
    partner_type = models.CharField(max_length=50)
    company_name = models.CharField(max_length=255)
    contact_phone = models.CharField(max_length=255, blank=True, null=True)
    contact_email = models.EmailField(max_length=255, blank=True, null=True)
    api_endpoint = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name

# class for address
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    street = models.CharField(max_length=255)
    village = models.CharField(max_length=100, blank=True, null=True)
    cell = models.CharField(max_length=100, blank=True, null=True)
    sector = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.street}, {self.district}, {self.country}"

# class for tax_information
class TaxInformation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tax_info')
    tin_number = models.CharField(max_length=50, unique=True)
    business_name = models.CharField(max_length=255, blank=True, null=True)
    tax_type = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"TIN: {self.tin_number} - {self.business_name}"

# class for user_settings
class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='settings')
    language = models.CharField(max_length=10, default='en')
    notifications_enabled = models.BooleanField(default=True)
    dark_mode = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Settings for {self.user.email}"

