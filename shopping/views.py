from django.shortcuts import render
from rest_framework import generics
from admins.serializers import ProductsAddSerializers
from .serializers import CartAddSerializers, CartAddListSerializers, CheckoutSerializer
from admins.models import ProductsModel
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from admins.views import CustomPagination
from django.shortcuts import get_object_or_404
from .models import CartModel, CheackoutModel, NEW
from rest_framework.views import APIView
from rest_framework import status
# Create your views here.
class ProductsViewListApi(generics.ListAPIView):
   serializer_class = ProductsAddSerializers
   queryset = ProductsModel.objects.all()
   permission_classes = [IsAuthenticated]
   
   
   
class ProductsViewDetailApi(generics.ListAPIView):
   serializer_class = ProductsAddSerializers
   queryset = ProductsModel.objects.all()
   permission_classes = [IsAuthenticated]
   
   def get(self, request, *args, **kwargs):
       instance = self.get_object()
       serializers = self.get_serializer(instance)
       return Response(serializers.data)
   
   
class ProductsSearchApi(generics.ListAPIView):
    serializer_class = ProductsAddSerializers
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    
    def get_queryset(self):
        queryset = ProductsModel.objects.all()
        search_query = self.request.query_params.get('q', None)
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        return queryset
    
    


class CartItemCreateAPIView(generics.CreateAPIView):
    queryset = CartModel.objects.all()
    serializer_class = CartAddSerializers

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class CartViewList(generics.ListAPIView):
    serializer_class = CartAddListSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartModel.objects.filter(user=self.request.user)
 
 
class CheckoutView(APIView):
    def post(self, request, pk):
        print(request.data)
        cart = get_object_or_404(ProductsModel, id=pk)
       
        phone = request.data.get('phone_number')
        addres = request.data.get('address')
        
        order = CheackoutModel.objects.create(
            product = cart,
            user=request.user,
            phone_number=phone,
            address=addres,
            status=NEW
        )

 
        serializers = CheckoutSerializer(order)

        return Response(serializers.data)
 
 

    
class ListallOrder(generics.ListAPIView):
    serializer_class = CheckoutSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return CheackoutModel.objects.filter(user=self.request.user)
    
    
class CartItemPlusView(generics.UpdateAPIView):
    queryset = CartModel.objects.all()
    serializer_class = CartAddSerializers

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.quantity += 1
        instance.save()
        return Response({"message": "Product quantity increased successfully."}, status=status.HTTP_200_OK)


class CartItemMinusView(generics.UpdateAPIView):
    queryset = CartModel.objects.all()
    serializer_class = CartAddSerializers

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.quantity > 1:
            instance.quantity -= 1
            instance.save()
            return Response({"message": "Product quantity decreased successfully."}, status=status.HTTP_200_OK)
        else:
            instance.delete()
            return Response({"message": "Product removed from cart because it reached minimum quantity."}, status=status.HTTP_204_NO_CONTENT)


class CartItemRemoveView(generics.DestroyAPIView):
    queryset = CartModel.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Product removed from cart successfully."}, status=status.HTTP_204_NO_CONTENT)