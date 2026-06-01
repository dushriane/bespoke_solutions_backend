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
    # this automatically fetches all nested placements related to this customization
    placements = DesignPlacementSerializer(many=True, read_only=True, source='designplacement_set')

    # this fetches the designer assignments tied to it
    assignments = DesignerAssignmentSerializer(many=True, read_only=True, source='designerassignment_set')

    # Optional: If you want to return the actual string names of the related products/designs 
    # instead of just their IDs, you can add fields like this:
    product_name = serializers.CharField(source='product.product_name', read_only=True)
    customer_email = serializers.CharField(source='customer.email', read_only=True)
    
    class Meta:
        model = DesignPlacement
        fields = '__all__'