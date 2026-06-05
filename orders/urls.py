from django.urls import path, include
from rest_framework.routers import DefaultRouter
from orders.views import (
    OrderViewSet, OrderItemViewSet,
    PaymentViewSet, ShipmentViewSet, ShipmentStatusHistoryViewSet
)

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'order-items', OrderItemViewSet, basename='order-item')
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'shipments', ShipmentViewSet, basename='shipment')
router.register(r'shipment-status', ShipmentStatusHistoryViewSet, basename='shipment-status')

urlpatterns = [
    path('', include(router.urls)),
]
