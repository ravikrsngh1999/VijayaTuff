from django.db import models
from django.contrib.auth.models import AbstractUser, User


class Size(models.Model):
    length = models.CharField(max_length=5)
    breadth = models.CharField(max_length=5)

    def __str__(self):
        return self.length + " X " + self.breadth



class GlassType(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name



class Product(models.Model):
    glass_type = models.ForeignKey(GlassType,on_delete=models.CASCADE)
    description = models.CharField(max_length=25)
    size = models.ForeignKey(Size,on_delete=models.CASCADE)
    quantity = models.CharField(max_length=5)

    def __str__(self):
        return self.glass_type.name + " - " + self.description + " - " + self.size.length + " X " + self.size.breadth



class Log(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    initial_quantity = models.CharField(max_length=5)
    in_quantity = models.CharField(max_length=5)
    used_quantity = models.CharField(max_length=5)
    left_quantity = models.CharField(max_length=5)
    date = models.CharField(max_length=15)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.product.glass_type.name + " - " + self.product.description + " - " + self.product.size.length + " X " + self.product.size.breadth
