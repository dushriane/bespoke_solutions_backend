from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomizationViewSet, DesignerAssignmentViewSet

router = DefaultRouter()
router.register(r'customizations', CustomizationViewSet, basename='customization')
router.register(r'assignments', DesignerAssignmentViewSet, basename='assignment')

urlpatterns = [
    path('', include(router.urls)),
]
