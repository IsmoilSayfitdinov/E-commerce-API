from django.shortcuts import render
from rest_framework import generics
from admins.serializers import ProductsViewSerializers, TagsSerializers, ComponeyNamesSerializers, SubCategorySerializer, CategorySerializer
from .serializers import AddToCartSerializers, CheckoutSerializers, ProductsSerializers,OrderSerializers, OrderItemSerializers, CartSerializers, CartItemSerializers
from admins.models import ProductsModel, Category, Tags, CamponeyaNames, Subcategory
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from admins.views import CustomPagination
from django.shortcuts import get_object_or_404
from .models import CartModel, Order, NEW, CartItem, OrderItem
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.
class ProductsViewListApi(generics.ListAPIView):
   serializer_class = ProductsViewSerializers
   queryset = ProductsModel.objects.all()
   filter_backends = [DjangoFilterBackend, OrderingFilter]
   filterset_fields = ['category', 'subcategory']
   ordering_fields = ['name', 'price']
  
   
class ProductsViewDetailApi(generics.RetrieveAPIView):
   serializer_class = ProductsViewSerializers
   queryset = ProductsModel.objects.all()
   permission_classes = [IsAuthenticated]
   
   
   
class ProductsSearchApi(generics.ListAPIView):
    serializer_class = ProductsViewSerializers
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    
    def get_queryset(self):
        queryset = ProductsModel.objects.all()
        search_query = self.request.query_params.get('q', None)
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        return queryset
    
    
class CartListApiView(generics.ListAPIView):
    serializer_class = CartSerializers
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return CartModel.objects.filter(user=self.request.user)
    
class AddToCartAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer  = AddToCartSerializers(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data.get('product_id')
            quantity = serializer.validated_data.get('quantity')
            
            product = ProductsModel.objects.get(id=product_id)
            cart, created = CartModel.objects.get_or_create(user=request.user)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            cart_item.quantity += quantity
            cart_item.save()
            return Response({"message": "Product added to cart successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CartCheckoutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        serializers = CheckoutSerializers(data=request.data)
        if serializers.is_valid():
            try:
                cart = CartModel.objects.get(id=pk, user=request.user)
            except:
                return Response({"message": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)
            phone_number = serializers.validated_data.get('phone_number')
            address = serializers.validated_data.get('address')
            total_price = sum(item.product.price * item.quantity for item in cart.items.all())
            order = Order.objects.create(user=request.user, phone_number=phone_number, address=address, total_price=total_price)
            for item in cart.items.all():
                OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.product.price * item.quantity)
            
            return Response({"message": "Order created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
class OrderListAPIView(generics.ListAPIView):
    serializer_class = OrderSerializers
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
        

    
class CartPlusProductAPIView(APIView):
    def post(self, request, pk, *args, **kwargs):
        cart = get_object_or_404(CartModel, user=request.user)
        cart_item = get_object_or_404(CartItem, cart=cart, product__id=pk)
        cart_item.quantity += 1
        cart_item.save()
        serializer = CartItemSerializers(cart_item)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CartMinusProductAPIView(APIView):
    def post(self, request, pk, *args, **kwargs):
        cart = get_object_or_404(CartModel, user=request.user)
        cart_item = get_object_or_404(CartItem, cart=cart, product__id=pk)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
            serializer = CartItemSerializers(cart_item)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            cart_item.delete()
            return Response({'detail': 'Product removed from cart.'}, status=status.HTTP_204_NO_CONTENT)

class CartRemoveProductAPIView(APIView):
    def post(self, request, pk, *args, **kwargs):
        cart = get_object_or_404(CartModel, user=request.user)
        cart_item = get_object_or_404(CartItem, cart=cart, product__id=pk)
        cart_item.delete()
        return Response({'detail': 'Product removed from cart.'}, status=status.HTTP_204_NO_CONTENT)

class TagsView(generics.ListAPIView):
    serializer_class = TagsSerializers
    queryset = Tags.objects.all()
    permission_classes = [AllowAny]
    
class CompaneyNamesView(generics.ListAPIView):
    serializer_class = ComponeyNamesSerializers
    queryset = CamponeyaNames.objects.all()
    permission_classes = [AllowAny]


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    

class CategoryDetailList(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]



class SubCategoryListView(generics.ListCreateAPIView):
    queryset = Subcategory.objects.all()
    serializer_class = SubCategorySerializer

