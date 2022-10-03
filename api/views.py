from django.shortcuts import render
from rest_framework.response import Response
from owner.models import *
from api.serializers import *
from rest_framework.viewsets import ModelViewSet
from rest_framework import authentication,permissions
from rest_framework.decorators import action


# Create your views here.

class UserRegistrationView(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class CategoryView(ModelViewSet):
     serializer_class = CategorySerializer
     queryset = Categories.objects.all()
     authentication_classes = [authentication.TokenAuthentication]
     permission_classes = [permissions.IsAuthenticated]

     @action(methods=["get"],detail=True)
     def get_product(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        category=Categories.objects.get(id=id)
        product=category.products_set.all()
        serializer=ProductSerializer(product,many=True)
        return Response(data=serializer.data)
     @action(methods=["post"],detail=True)
     def add_product(self,request,*args,**kwargs):
        id = kwargs.get("pk")
        category = Categories.objects.get(id=id)
        id = kwargs.get("pk")
        serializer=ProductSerializer(data=request.data,context={"category":category})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)




class ProductView(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Products.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=["post"], detail=True)
    def add_to_cart(self, request, *args, **kwargs):
        user = request.user
        id = kwargs.get("pk")
        product = Products.objects.get(id=id)
        serializer = CartSerializer(data=request.data, context={"user": user, "product": product})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    @action(methods=["post"], detail=True)
    def add_review(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        product = Products.objects.get(id=id)
        user = request.user
        serializer = ReviewSerializer(data=request.data, context={"user": user, "product": product})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    @action(methods=["get"], detail=True)
    def get_review(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        product = Products.objects.get(id=id)
        reviews = product.reviews_set.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(data=serializer.data)


class CartsView(ModelViewSet):
    serializer_class = CartSerializer
    queryset = Carts.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]









