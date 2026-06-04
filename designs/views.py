from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Design
from .serializers import DesignSerializer

class DesignViewSet(viewsets.ModelViewSet):
    queryset = Design.objects.all()
    serializer_class = DesignSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "put", "delete"]

    def get_queryset(self):
        user = self.request.user
        if getattr(self, 'swagger_fake_view', False):
            return Design.objects.none()
        
        if user.is_staff:
            return Design.objects.all().order_by('-created_at')
        return Design.objects.filter(uploaded_by=user).order_by('-created_at')
    
    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)
