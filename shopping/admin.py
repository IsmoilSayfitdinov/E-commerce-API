from django.contrib import admin
from .models import ProductsModel, CartModel, CartItem, Order, OrderItem


admin.site.register(ProductsModel)
admin.site.register(CartModel)
admin.site.register(Order)
admin.site.register(CartItem)
admin.site.register(OrderItem)