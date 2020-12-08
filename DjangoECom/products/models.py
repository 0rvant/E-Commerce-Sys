from django.db import models
from django.contrib.auth.models import User
#from .models import Customer
# Create your models here.
label_choices = (
    ('S', 'Standard'),
    ('N', 'New'),
    ('B', 'Best Selling')
)


class Category(models.Model):
    pass
class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(blank=False)
    image = models.ImageField()
    description = models.TextField(max_length=256, null=True) 
    review = models.IntegerField()
    discount_price = models.FloatField(null=True, blank=True)
    quantity = models.IntegerField()
    label = models.CharField(choices=label_choices, max_length=1)
    category = models.ManyToManyField(Category, related_name="category_name")
    seller = models.ForeignKey(User, related_name="seller_name", on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class OrderProduct(models.Model):
    #product = models.ForeignKey(Product, related_name="")
    pass


class Order(models.Model):
    pass
