from django.contrib import admin
from accounts.models import *
admin.site.register(User)
admin.site.register(VerificationCode)
admin.site.register(Designer)
admin.site.register(ExternalPartner)
admin.site.register(Address)
admin.site.register(UserSettings)
admin.site.register(TaxInformation)