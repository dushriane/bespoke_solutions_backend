from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Product, ProductCategory, ProductVariant
from .serializers import ProductCategorySerializer, ProductSerializer, ProductVariantSerializer

class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Product.objects.all()
        category = self.request.query_params.get('category')
        is_active = self.request.query_params.get('is_active')

        if category is not None:
            queryset = queryset.filter(category_id = category)
        if is_active is not None:
            is_active_bool = str(is_active).lower() == 'true'
            queryset = queryset.filter(is_active=is_active_bool)
        return queryset

class ProductVariantViewSet(viewsets.ModelViewSet):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    