from rest_framework import serializers
from .models import Customization, DesignPlacement, DesignerAssignment

class DesignPlacementSerializer(serializers.ModelSerializer):
    class Meta:
        model = DesignPlacement
        fields = '__all__'

class DesignerAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DesignerAssignment
        fields = '__all__'

class CustomizationSerializer(serializers.ModelSerializer):
    placements = DesignPlacementSerializer(many=True, read_only=True, source='designplacement_set')
    assignments = DesignerAssignmentSerializer(many=True, read_only=True, source='designerassignment_set')
    product_name = serializers.CharField(source='product.product_name', read_only=True)
    customer_email = serializers.CharField(source='customer.email', read_only=True)

    class Meta:
        model = Customization
        fields = '__all__'
        read_only_fields = ['customer']