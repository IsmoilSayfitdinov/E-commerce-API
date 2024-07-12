from rest_framework import serializers
from .models import ProductsModel
from shopping.models import CheackoutModel
class ProductsAddSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductsModel
        fields = "__all__"
        
        
class OrderStatusUdpateSerializers(serializers.ModelSerializer):
    ACCEPTED = 'ACCEPTED'

    class Meta:
        model = CheackoutModel
        fields = ('status',) 

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance