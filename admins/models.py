from django.db import models
from shared.models import BaseModel
# Create your models here.
class ProductsModel(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField()
    photo = models.ImageField(upload_to='products')
    quantity = models.IntegerField()
    
    
    def __str__(self) -> str:
        return self.name
