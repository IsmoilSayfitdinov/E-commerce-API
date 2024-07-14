from .models import CartModel, CartItem, Order, OrderItem
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


class CartItemSerializers(serializers.ModelSerializer):
    product = ProductsSerializers()
    class Meta:
        model = CartItem
        fields = ['product', 'quantity']
        
class CartSerializers(serializers.ModelSerializer):
    items = CartItemSerializers(many=True)
    
    class Meta:
        model = CartModel
        fields = ["id",'items']
        
class AddToCartSerializers(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    
class CheckoutSerializers(serializers.Serializer):
    phone_number = serializers.CharField()
    address = serializers.CharField()
    
class OrderItemSerializers(serializers.ModelSerializer):
    product = ProductsSerializers()
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', "price"]
        
class OrderSerializers(serializers.ModelSerializer):
    items = OrderItemSerializers(many=True)
    class Meta:
        model = Order
        fields = ['id', 'items', 'phone_number', 'address', 'status', "total_price"]