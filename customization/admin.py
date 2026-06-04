from django.contrib import admin
from customization.models import Customization, DesignerAssignment, DesignPlacement
admin.site.register(Customization)
admin.site.register(DesignPlacement)
admin.site.register(DesignerAssignment)