from django.db import models
from django.contrib.auth.models import User
#from users.models import Customer
# Create your models here.
class Product(models.Model):
    label_choices = (
        ('S', 'Standard'),
        ('N', 'New'),
        ('B', 'Best Selling')
    )
    category_choices = (
        ('C', 'Clothes'),
        ('M', 'Mobiles'),
        ('T', 'TVs')
    )
    seller = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(blank=False)
    quantity = models.IntegerField()    
    discount_price = models.FloatField(null=True, blank=True)
    description = models.TextField(max_length=500, null=True)
    image = models.ImageField(blank=True, null=True)
    date_created = models.DateField(auto_now_add=True, null=True)
    label = models.CharField(choices=label_choices, max_length=1, default='S')
    category = models.CharField(choices=category_choices, max_length=2, null=True)
    review = models.FloatField(default=0)

    def __str__(self):
        return self.name

class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    def __str__(self):
        return self.product.name

class Order(models.Model):
    customer = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    order = models.ManyToManyField(Cart)
    start_date = models.DateField(auto_now_add=True, null=True)
    ordered_date = models.DateField(null=True)
    ordered = models.BooleanField(default=False)
    def __str__(self):
        return self.customer.username
