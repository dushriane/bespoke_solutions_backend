from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Bespoke Solutions API",
        default_version="v1",
        description="API Documentation for the Bespoke Solutions platform.",
        contact=openapi.Contact(email="contact@bespokesolutions.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Core API routes
    path('api/auth/', include('accounts.urls')),
    path('api/products/', include('product.urls')),
    path('api/designs/', include('designs.urls')),
    path('api/customization/', include('customization.urls')),
    path('api/cart/', include('cart.urls')),
    path('api/orders/', include('orders.urls')),

    # Docs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
