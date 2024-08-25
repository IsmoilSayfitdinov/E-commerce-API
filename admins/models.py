from django.db import models
from shared.models import BaseModel



class Category(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self) -> str:
        return self.name
    

class Subcategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    def __str__(self) -> str:
        return self.name


class Tags(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return self.name    

class CamponeyaNames(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return self.name
    
class ProductsModel(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField()
    photo = models.ImageField(upload_to='products')
    quantity = models.IntegerField()
    tags = models.ManyToManyField(Tags, null=True)
    camponeya_names = models.ForeignKey(CamponeyaNames , on_delete=models.CASCADE, null=True, blank=True)
    discount = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, null=True, blank=True, related_name="products")
    
  
    
    def __str__(self) -> str:
        return self.name

    @property
    def discounted_price(self):
        if self.discount > 0:
            return self.price * (1 - self.discount / 100)
        return self.price
    
    @property
    def discount_percentage(self):
        return self.discount