from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomizationViewSet, DesignPlacementViewSet, DesignerAssignmentViewSet

router = DefaultRouter()
router.register(r'customizations', CustomizationViewSet)
router.register(r'placements', DesignPlacementViewSet)
router.register(r'assignments', DesignerAssignmentViewSet)

urlpatterns = [
    path('', include(router.urls)), 
]