from rest_framework import serializers
from .models import ProductsModel
from shopping.models import Order
class ProductsAddSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductsModel
        fields = "__all__"
        
        
class OrderStatusUdpateSerializers(serializers.ModelSerializer):
    ACCEPTED = 'ACCEPTED'

    class Meta:
        model = Order
        fields = ('status',) 

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance