from rest_framework import serializers
from owner.models import *
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=[
            "first_name",
            "last_name",
            "email",
            "password",
            "username"
        ]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model=Categories
        fields="__all__"

class ProductSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    category=serializers.CharField(read_only=True)
    class Meta:
        model=Products
        fields=[
            "id",
            "product_name",
            "category",
            "image",
            "price",
            "description"

        ]


class CartSerializer(serializers.ModelSerializer):
    product=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)

    class Meta:
        model=Carts
        fields="__all__"

    def create(self,validated_data):
        user=self.context.get("user")
        product=self.context.get("product")
        return Carts.objects.create(**validated_data,user=user,product=product)


class ReviewSerializer(serializers.ModelSerializer):
    product = serializers.CharField(read_only=True)
    user = serializers.CharField(read_only=True)
    class Meta:
        model=Reviews
        fields="__all__"

    def create(self, validated_data):
        user=self.context.get("user")
        product=self.context.get("product")
        return Reviews.objects.create(user=user,product=product,**validated_data)