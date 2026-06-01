from django.urls import path, include
from accounts.views import (
    UserViewSet, 
    LoginMixin, 
    VerifyAccountView, 
    RequestPasswordResetView, 
    ResetPasswordView
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginMixin.as_view(), name='login'),
    path('verify-account/', VerifyAccountView.as_view(), name='verify-account'),
    path('request-password-reset/', RequestPasswordResetView.as_view(), name='request-password-reset'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
]
