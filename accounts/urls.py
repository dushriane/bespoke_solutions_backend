from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts.views import (
    AddressViewSet,
    UserViewSet,
    RegisterView,
    LoginMixin,
    RequestPasswordResetView,
    ResetPasswordView,
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginMixin.as_view(), name='login'),
    path('request-password-reset/', RequestPasswordResetView.as_view(), name='request-password-reset'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('addresses/<int:pk>/set_default/', AddressViewSet.as_view({'post': 'set_default'}), name='address-set-default'),
]
