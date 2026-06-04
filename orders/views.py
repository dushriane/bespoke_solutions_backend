from django.shortcuts import render
from rest_framework import viewsets
from orders.models import Order, OrderItem, Payment, Shipment, ShipmentStatusHistory
from orders.serializers import OrderSerializer, OrderItemSerializer, PaymentSerializer, ShipmentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order_item = serializer.save()
        return Response(OrderItemSerializer(order_item).data, status=status.HTTP_201_CREATED)