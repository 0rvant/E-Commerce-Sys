from django.db import models

# Create your models here.
class Customer(models.Model):
    firstname = models.CharField(max_length=10)
    seconedname = models.CharField(max_length=10)
    username = models.CharField(max_length=64, unique=True)
    email = models.EmailField(max_length=128, unique=True)
    password = models.CharField(max_length=64)
    phone = models.IntegerField(max_length=12)

class Seller(models.Model):
    firstname = models.CharField(max_length=10)
    seconedname = models.CharField(max_length=10)
    username = models.CharField(max_length=64, unique=True)
    email = models.EmailField(max_length=128, unique=True)
    password = models.CharField(max_length=64)
    phone = models.IntegerField(max_length=12)