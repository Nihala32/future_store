from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator,MaxValueValidator


# Create your models here.

class Categories(models.Model):
    category_name=models.CharField(max_length=120,unique=True)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.category_name


class Products(models.Model):
    product_name=models.CharField(max_length=120,unique=True)
    category=models.ForeignKey(Categories,on_delete=models.CASCADE)
    image=models.ImageField( upload_to="Images", null=True)
    price=models.PositiveIntegerField()
    description=models.CharField( max_length=250,null=True)

    def __str__(self):
        return self.product_name


class Carts(models.Model):
    product=models.ForeignKey(Products, on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    created_date=models.DateTimeField(auto_now_add=True,null=True)
    options=(
        ("incart","incart"),
       ( "order placed","order placed"),
        ("cancelled","cancelled"),

    )
    status=models.CharField(max_length=120,choices=options,default="incart")
    quantity=models.PositiveIntegerField(default=1)

class Orders(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    created_date=models.DateTimeField(auto_now_add=True,null=True)
    options=(
        ("order-placed","order-placed"),
        ("dispatched","dispatched"),
        ("in-transit","in-transit"),
        ("delivered","delivered"),
        ("cancelled","cancelled")
    )
    status=models.CharField(max_length=120,choices=options,default="order-placed")
    delivery_address=models.CharField(max_length=120,null=True)
    expected_date=models.DateField(null=True)



class Reviews(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    comments=models.CharField(max_length=120)
    rating=models.PositiveIntegerField([MinValueValidator(1),MaxValueValidator(5)])


    





