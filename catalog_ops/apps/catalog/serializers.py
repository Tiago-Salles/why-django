from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='name_md5')
    
    class Meta:
        model = Product
        fields = [
            'uuid', 'name', 'price', 'is_active',
            'quantity', 'description', 'created_at', 'updated_at'
        ]
