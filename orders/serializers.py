from rest_framework import serializers
from orders.models import Order, OrderItem, Payment, Shipment, ShipmentStatusHistory

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'
    
class PaymentSerializer(serializers.ModelSerializer):
    payment_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    #momo pay or card pay
    payment_method = serializers.CharField(max_length=50 )
    card_number = serializers.CharField(max_length=16, required=False, allow_blank=True)
    Momo_number = serializers.CharField(max_length=13, required=False, allow_blank=True)
    class Meta:
        model = Payment
        fields = '__all__'

class ShipmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shipment
        fields = '__all__'

class ShipmentStatusHistorySerializer(serializers.ModelSerializer):
    status = serializers.CharField(max_length=50, help_text="status= shipped, delivered, in transit")
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    class Meta:
        model = ShipmentStatusHistory
        fields = '__all__'

    def create(self, validated_data):
        shipment = validated_data['shipment']
        status = validated_data['status']    
        ShipmentStatusHistory.objects.create(shipment=shipment, status=status)
        return validated_data


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)
    shipments = ShipmentSerializer(many=True, read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        payments_data = validated_data.pop('payments', [])
        shipments_data = validated_data.pop('shipments', [])

        order = Order.objects.create(**validated_data)

        for item in items_data:
            OrderItem.objects.create(order=order, **item)
        for payment in payments_data:
            Payment.objects.create(order=order, **payment)
        for shipment in shipments_data:
            Shipment.objects.create(order=order, **shipment)

        return order