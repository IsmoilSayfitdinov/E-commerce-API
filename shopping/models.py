from django.db import models
from shared.models import BaseModel
from admins.models import ProductsModel
from users.models import UserModel


    
class CartModel(BaseModel):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.user.username
    
class CartItem(BaseModel):
    cart = models.ForeignKey(CartModel, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(ProductsModel, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    def __str__(self) -> str:
        return self.product.name
    
NEW, ACCEPTED = 'NEW', 'ACCEPTED'
class Order(BaseModel):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    status = models.CharField(max_length=255, default=NEW)
    total_price = models.IntegerField()

    def __str__(self) -> str:
        return self.cart.user.username
class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(ProductsModel, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()
    
    def __str__(self) -> str:
        return f"{self.product.name} - {self.user}"