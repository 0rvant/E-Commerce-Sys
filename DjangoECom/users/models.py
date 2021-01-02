from django.db import models
from django.contrib.auth.models import User
from currencies.models import Currency

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=12, blank=False)
    isseller = models.BooleanField(default=False)
    image = models.ImageField(default="profile_pic.png")
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, default='USD')
    new = models.BooleanField(default = True, null=True, blank =False)

    def __str__(self):
        return self.user.username
    