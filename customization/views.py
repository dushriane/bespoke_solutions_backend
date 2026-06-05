from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Customization, DesignPlacement, DesignerAssignment
from .serializers import CustomizationSerializer, DesignerAssignmentSerializer, DesignPlacementSerializer


class CustomizationViewSet(viewsets.ModelViewSet):
    serializer_class = CustomizationSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "put", "delete"]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Customization.objects.none()
        user = self.request.user
        if user.is_staff:
            return Customization.objects.all().order_by('-created_at')
        return Customization.objects.filter(customer=user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def update_status(self, request, pk=None):
        customization = self.get_object()
        new_status = request.data.get('status')
        if not new_status:
            return Response({'error': 'No status provided'}, status=status.HTTP_400_BAD_REQUEST)
        customization.status = new_status
        customization.save()
        return Response({'status': f'Status updated to {new_status}'})

    @action(detail=True, methods=['get', 'post'], permission_classes=[permissions.IsAuthenticated])
    def placements(self, request, pk=None):
        """List or create placements for a specific customization"""
        customization = self.get_object()
        if request.method == 'GET':
            placements = DesignPlacement.objects.filter(customization=customization)
            return Response(DesignPlacementSerializer(placements, many=True).data)
        serializer = DesignPlacementSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(customization=customization)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DesignerAssignmentViewSet(viewsets.ModelViewSet):
    """Admin/staff only: assign designers to customizations"""
    serializer_class = DesignerAssignmentSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff and not user.is_superuser:
            return DesignerAssignment.objects.filter(designer=user).order_by('deadline')
        return DesignerAssignment.objects.all().order_by('deadline')
