from django.urls import path
from rest_framework.routers import DefaultRouter
from api.views import *
from rest_framework.authtoken.views import obtain_auth_token

router=DefaultRouter()
router.register('category',CategoryView,basename="categories")
router.register('products',ProductView,basename="products")
router.register('accounts/signup',UserRegistrationView,basename='register')
router.register('carts',CartsView,basename='carts')




urlpatterns=[
                path('accounts/token', obtain_auth_token),

            ]+router.urls