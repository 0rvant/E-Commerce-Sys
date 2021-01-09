

from django.db import models
from django.contrib.auth.models import User
from users.models import Customer
# Create your models here.



class Product(models.Model):
    label_choices = (
        ('Standard', 'Standard'),
        ('New', 'New'),
        ('Best Selling', 'Best Selling')
    )
    category_choices = (
        ('Clothes', 'Clothes'),
        ('Mobiles', 'Mobiles'),
        ('TVs', 'TVs')
    )
    seller = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(blank=False)
    digital = models.BooleanField(default = False, null=True, blank =False)
    quantity = models.IntegerField()    
    discount_price = models.FloatField(null=True, blank=True)
    description = models.TextField(max_length=500, null=True)
    image = models.ImageField(blank=True, null=True,upload_to='media/')
    date_created = models.DateField(auto_now_add=True, null=True)
    label = models.CharField(choices=label_choices, max_length=20, default='New')
    category = models.CharField(choices=category_choices, max_length=20, null=True)
    total_review = models.IntegerField(default=1)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):    #for product in products ----> product.imageURL to display image in frontend
        try:
            url =self.image.url
        except:
            url = ''
        return url

class Review(models.Model):
    STATUS = (
        ('True','True'),
        ('False','False'),
        ('New','New'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=250, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default='New')
    subject = models.CharField(max_length=50, blank=True)
    ip = models.CharField(max_length=20, blank=True)
    rate = models.IntegerField(default=1)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
    
class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL, blank=True,null=True)
    date_ordered=models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,null=True,blank=False)
    transaction_id=models.CharField(max_length=200,null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping


    @property
    def get_cart_total_discount(self):
        orderitems =self.orderitem_set.all()
        total =sum([item.get_total_discount for item in orderitems])
        return total

    @property
    def get_cart_total(self):
        orderitems =self.orderitem_set.all()
        total =sum([item.get_total for item in orderitems])
        return total
    @property
    def get_cart_items(self):
        orderitems =self.orderitem_set.all()
        total =sum([item.quantity for item in orderitems])
        return total
    @property
    def cart_discount(self):
        orderitems =self.orderitem_set.all()
        discount =sum([item.get_total for item in orderitems])-sum([item.get_total_discount for item in orderitems])
        return discount

class OrderItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,blank=True,null=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total =self.product.price * self.quantity
        return total

    @property
    def get_total_discount(self):
        total =self.product.discount_price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address


class WishList(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL, blank=True,null=True)
    def __str__(self):
        return str(self.id)

class WishListItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    wishList = models.ForeignKey(WishList, on_delete=models.SET_NULL, blank=True, null=True)
