from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from .models import ProductsModel
from .serializers import ProductsAddSerializers, OrderStatusUdpateSerializers
from rest_framework import generics, pagination
from users.models import UserModel
from users.serializer import UserUpdateSerializer
from shopping.serializers import CheckoutSerializer
from shopping.models import CheackoutModel, ACCEPTED

class ProductsAddView(APIView):
    permission_classes = [IsAdminUser]
    serializer_class = ProductsAddSerializers
    
    def post(self, requset):
        serializer = self.serializer_class(data=requset.data)
        if serializer.is_valid():
            serializer.save()
            response = {
			"status": True,
			"message": "added",
			"data": serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class ProductsUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = ProductsAddSerializers
    queryset = ProductsModel.objects.all()
    
    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
			"status": True,
			"message": "Updated",
			"data": serializer.data
		    } 
        
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response = {
			"status": True,
			"message": "Updated",
			"data": serializer.data
		    } 
        
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProductsDelete(generics.DestroyAPIView):
    serializer_class = ProductsAddSerializers
    queryset = ProductsModel.objects.all()
    permission_classes = [IsAdminUser]
    
    def delete(self, request, *args, **kwargs):
        super(ProductsDelete, self).delete(request, *args, **kwargs)
        response = {
			"status": True,
			"message": "Deleted"
		}
        return Response(response, status=status.HTTP_200_OK)
    

class ProductsDetailView(generics.ListAPIView):
    serializer_class = ProductsAddSerializers
    queryset = ProductsModel.objects.all()
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    
class CustomPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class UserListView(generics.ListAPIView):
    serializer_class = UserUpdateSerializer
    queryset = UserModel.objects.all()
    permission_classes = [IsAdminUser]
    pagination_class = CustomPagination
    
    
    
class UserListDetailApiView(generics.ListAPIView):
    serializer_class = UserUpdateSerializer
    queryset = UserModel.objects.all()
    permission_classes = [IsAdminUser]
    pagination_class = CustomPagination
    
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class ListOneUserOrders(generics.ListAPIView):
    serializer_class = CheckoutSerializer
    permission_classes = [IsAdminUser]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user 
        product_pk = self.kwargs['pk']

        queryset = CheackoutModel.objects.filter(user=user, product=product_pk)
        return queryset
    
class ViewAllOrders(generics.ListAPIView):
    serializer_class = CheckoutSerializer
    permission_classes = [IsAdminUser]
    queryset = CheackoutModel.objects.all()
    
    
class UserOrderUpdateView(generics.UpdateAPIView):
    serializer_class = OrderStatusUdpateSerializers
    permission_classes = [IsAdminUser]
    queryset = CheackoutModel.objects.all()
    

    def put(self, request, pk,*args, **kwargs):
        checkout = CheackoutModel.objects.filter(user=request.user, pk=pk)
        
        if checkout:
            checkout.update(status=ACCEPTED)
            res = {
                "status": True,
                "message": "Accepted"
            }
            return Response(res,status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
