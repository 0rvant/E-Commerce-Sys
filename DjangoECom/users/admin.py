from django.contrib import admin
from .models import Customer
from products.models import *
# Register your models here.

admin.site.register(Customer)
admin.site.register(WishList)
admin.site.register(WishListItem)
admin.site.register(ShippingAddress)