from django.db import models

# Create your models here.
class Register(models.Model):
    Username = models.CharField(max_length=30)
    Email = models.EmailField()
    Password = models.CharField(max_length=30)


class Products(models.Model):
    Name = models.CharField(max_length=20)
    Type = models.CharField(max_length=20)
    Price = models.DecimalField(max_digits=5, decimal_places=2)
    Description = models.CharField(max_length=200)
    image = models.ImageField(upload_to="images/", height_field=None,width_field=None,max_length=100)
