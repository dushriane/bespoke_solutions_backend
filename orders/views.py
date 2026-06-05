from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from orders.models import Order, OrderItem, Payment, Shipment, ShipmentStatusHistory
from orders.serializers import (
    OrderSerializer, OrderItemSerializer,
    PaymentSerializer, ShipmentSerializer, ShipmentStatusHistorySerializer
)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all().order_by('-created_at')
        return Order.objects.filter(name=user.full_name).order_by('-created_at')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class OrderItemViewSet(viewsets.ModelViewSet):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return OrderItem.objects.filter(order__in=Order.objects.all())


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Payment.objects.all()
        return Payment.objects.filter(order__name=user.full_name)


class ShipmentViewSet(viewsets.ModelViewSet):
    """Admin/staff only: manage shipments"""
    serializer_class = ShipmentSerializer
    permission_classes = [IsAdminUser]
    queryset = Shipment.objects.all()


class ShipmentStatusHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only shipment tracking"""
    serializer_class = ShipmentStatusHistorySerializer
    permission_classes = [IsAuthenticated]
    queryset = ShipmentStatusHistory.objects.all().order_by('-updated_at')
