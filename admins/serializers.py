from rest_framework import serializers
from .models import ProductsModel, Category, Tags, CamponeyaNames, Subcategory
from shopping.models import Order

class TagsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = "__all__"
        

class ComponeyNamesSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = CamponeyaNames
        fields = "__all__"



class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = '__all__'
    
class ProductsAddSerializers(serializers.ModelSerializer):
    
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    subcategory = serializers.PrimaryKeyRelatedField(queryset=Subcategory.objects.all())
    camponeya_names = serializers.PrimaryKeyRelatedField(
        queryset=CamponeyaNames.objects.all(),  # Bu yerda queryset to'g'ri o'rnatilgan
        required=False,  # Agar ushbu maydon ixtiyoriy bo'lsa
    )
    tags = serializers.PrimaryKeyRelatedField(queryset=Tags.objects.all(), many=True)
    
    class Meta:
        model = ProductsModel
        fields = '__all__'
        
        
class ProductsViewSerializers(serializers.ModelSerializer):   
    
    discounted_price = serializers.ReadOnlyField()
    discount_percentage = serializers.ReadOnlyField()
    
    category = CategorySerializer(required=True)
    subcategory = SubCategorySerializer(required=True)
    class Meta:
        model = ProductsModel
        fields = ['id', 'name', "quantity","description",'price', 'photo', "category", "subcategory",'discounted_price', 'discount_percentage',"camponeya_names"]

    
    
        
class OrderStatusUdpateSerializers(serializers.ModelSerializer):
    ACCEPTED = 'ACCEPTED'

    class Meta:
        model = Order
        fields = ('status',) 

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance