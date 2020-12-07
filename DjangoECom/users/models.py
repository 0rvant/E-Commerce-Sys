from django.db import models
# Create your models here.
class Customer(models.Model):
    firstname = models.CharField(max_length=10,null=True)
    secondname = models.CharField(max_length=10,null=True)
    username = models.CharField(max_length=64, unique=True,null=True)
    email = models.EmailField(max_length=128, unique=True,null=True)
    password = models.CharField(max_length=64,null=True)
    phone = models.IntegerField(null=True)

class Seller(models.Model):
    firstname = models.CharField(max_length=10,null=True)
    secondname = models.CharField(max_length=10,null=True)
    username = models.CharField(max_length=64, unique=True,null=True)
    email = models.EmailField(max_length=128, unique=True,null=True)
    password = models.CharField(max_length=64,null=True)
    phone = models.IntegerField(null=True)