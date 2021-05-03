from django.db import models
from django.contrib.auth.models import AbstractUser, User


class Size(models.Model):
    length = models.CharField(max_length=5)
    breadth = models.CharField(max_length=5)

    def __str__(self):
        return self.length + " X " + self.breadth




class GlassType(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name



class Product(models.Model):
    glass_type = models.ForeignKey(GlassType,on_delete=models.CASCADE)
    description = models.CharField(max_length=25)
    size = models.ForeignKey(Size,on_delete=models.CASCADE)
    quantity = models.CharField(max_length=5)

    def __str__(self):
        return self.glass_type.name + " - " + self.description + " - " + self.size.length + " X " + self.size.breadth



class OffCutProduct(models.Model):
    glass_type = models.ForeignKey(GlassType,on_delete=models.CASCADE)
    description = models.CharField(max_length=25)
    length = models.CharField(max_length=5)
    breadth = models.CharField(max_length=5)
    quantity = models.CharField(max_length=5,default="0")

    def __str__(self):
        return self.glass_type.name + " - " + self.description + " - " + self.length + " X " + self.breadth



class Log(models.Model):
    glass_type = models.CharField(max_length=30)
    description = models.CharField(max_length=25)
    size = models.CharField(max_length=15,default="None")
    initial_quantity = models.CharField(max_length=5)
    in_quantity = models.CharField(max_length=5)
    used_quantity = models.CharField(max_length=5)
    left_quantity = models.CharField(max_length=5)
    date = models.CharField(max_length=15)
    offcut = models.BooleanField(default=False)
    remarks = models.CharField(max_length=2500,default="No Remark")
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.glass_type + " - " + self.description + " - " + self.size + " - " + self.date
