from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=12, blank=False)
    isseller = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    