from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Customization, DesignPlacement, DesignerAssignment
from .serializers import CustomizationSerializer, DesignerAssignmentSerializer, DesignPlacementSerializer

class CustomizationViewSet(viewsets.ModelViewSet):
    queryset = Customization.objects.all().order_by('-created_at')
    serializer_class = CustomizationSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "put", "delete"]

    def get_queryset(self):
        user = self.request.user
        if getattr(self, 'swagger_fake_view', False):
            return Customization.objects.none()
        
        if user.is_staff:
            return Customization.objects.all().order_by('-created_at')
        return Customization.objects.filter(customer=user).order_by('-created_at')
    
    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        customization = self.get_object()
        new_status = request.data.get('status')
        if new_status:
            customization.status = new_status
            customization.save()
            return Response({'status': 'Status updated tp {}'.format(new_status)})
        return Response({'error': 'No status provided'}, status=status.HTTP_400_BAD_REQUEST)
    
class DesignPlacementViewSet(viewsets.ModelViewSet):
    queryset = DesignPlacement.objects.all()
    serializer_class = DesignPlacementSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "put", "delete"]

class DesignerAssignmentViewSet(viewsets.ModelViewSet):
    queryset = DesignerAssignment.objects.all()
    serializer_class = DesignerAssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "put", "delete"]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff and not user.is_superuser:
            return DesignerAssignment.objects.filter(designer=user).order_by('deadline')
        return DesignerAssignment.objects.all().order_by('deadline')