from rest_framework import serializers
from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            'id',
            'cart',
            'product_name',
            'quantity',
            'price',
            'total_price',
        ]
        read_only_fields = ['id']

    def get_total_price(self, obj):
        return obj.quantity * obj.price


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_items = serializers.SerializerMethodField()
    cart_total = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Cart
        fields = [
            'id',
            'cart_id',
            'created_at',
            'updated_at',
            'items',
            'total_items',
            'cart_total',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_total_items(self, obj):
        return sum(item.quantity for item in obj.items.all())

    def get_cart_total(self, obj):
        return sum(item.quantity * item.price for item in obj.items.all())
