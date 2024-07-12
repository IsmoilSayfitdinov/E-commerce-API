from .models import CartModel, CheackoutModel
from rest_framework import serializers
from users.models import UserModel
from admins.models import ProductsModel

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['uuid', 'username']

class ProductsSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductsModel
        fields = ['id', 'name', 'description', 'price', 'photo']

class CartAddSerializers(serializers.ModelSerializer):
    
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = CartModel
        fields = ['products', 'quantity', "user"]
        
        
class CartAddListSerializers(serializers.ModelSerializer):
    user = UserSerializer()
    products = ProductsSerializers(read_only=True)
    
    class Meta:
        model = CartModel
        fields = ['user', 'products', 'quantity']
        
class CheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheackoutModel
        fields = ['phone_number', 'address', 'user', 'product', 'status']