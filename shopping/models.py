from django.db import models
from shared.models import BaseModel
from admins.models import ProductsModel
from users.models import UserModel

class CartModel(BaseModel):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    products = models.ForeignKey(ProductsModel, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    

NEW, VERIFYD ,ACCEPTED = 'NEW', "VERIFYD",'ACCEPTED'
  
class CheackoutModel(BaseModel):
    
    STATUS = (
        (NEW, NEW),
        (VERIFYD, VERIFYD),
        (ACCEPTED, ACCEPTED)
    )
    
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductsModel, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    status = models.CharField(max_length=255, choices=STATUS, default=NEW)
    def __str__(self) -> str:
        return self.phone_number
    
    