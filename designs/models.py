from django.db import models
from accounts.models import User

# Create your models here.
class Design(models.Model):
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    design_name = models.CharField(max_length=255, null=True, blank=True)
    file_name = models.CharField(max_length=255)
    file_url = models.TextField()
    file_type = models.CharField(max_length=50, null=True, blank=True)
    preview_image = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.design_name or self.file_name

