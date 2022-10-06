from django.shortcuts import render,redirect
from owner.models import *
from django.contrib.auth.models import User
from django.views.generic import CreateView,TemplateView,View,FormView,DetailView,ListView,UpdateView
from customer import forms
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.core.mail import send_mail

# Create your views here.

class RageistrationView(CreateView):
    form_class = forms.UserRegistrationForm
    template_name = "registration.html"
    success_url = reverse_lazy("login")

class LoginView(FormView):
    template_name = "login.html"
    form_class = forms.LoginForm

    def post(self,request,*args,**kwargs):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get("username")
            password=form.cleaned_data.get("password")
            user=authenticate(request,username=username,password=password)
            if user:
                login(request,user)
                if request.user.is_superuser:
                    messages.success(request, "")
                    return redirect("dashboard")
                else:
                    return redirect("home")
            else:
                messages.error(request, "invalid credentials")
                return render(request,"login.html",{"form":form})

class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        all_products=Products.objects.all()
        context["products"]=all_products
        return context


class ProductDetailView(DetailView):
    template_name = "product-detail.html"
    model = Products
    context_object_name = "product"
    pk_url_kwarg = "id"

class AddToCartView(FormView):
    template_name = "addto-cart.html"
    form_class = forms.CartForm


    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        product=Products.objects.get(id=id)
        return render(request,self.template_name,{"form":forms.CartForm,"product":product})

    def post(self,request,*args,**kwargs):
        id = kwargs.get("id")
        product = Products.objects.get(id=id)
        quantity=request.POST.get("quantity")
        user=request.user
        Carts.objects.create(product=product,user=user,quantity=quantity)
        messages.success(self.request, "")
        return redirect("home")


class MyCartView(ListView):
    model = Carts
    template_name = "cart-list.html"
    context_object_name = "carts"

    def get_queryset(self):
        return Carts.objects.filter(user=self.request.user).exclude(status="cancelled").order_by("-created_date")



class CartRemoveView(ListView):
    template_name = "cart-remove.html"
    form_class = forms.CartForm
    context_object_name = "carts"

    def get_queryset(self):
        id=self.kwargs.get("id")
        cart=Carts.objects.get(id=id)
        cart.status="cancelled"
        cart.delete()
        messages.success(self.request,"removed successfully")
        return Carts.objects.filter(user=self.request.user).exclude(status="cancelled").order_by("-created_date")



class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")


class PlaceOrderView(FormView):
    template_name = "place-order.html"
    form_class = forms.OrderForm

    def post(self,request,*args,**kwargs):
        cart_id=kwargs.get("cid")
        product_id=kwargs.get("pid")
        cart=Carts.objects.get(id=cart_id)
        product=Products.objects.get(id=product_id)
        user=request.user
        delivery_address=request.POST.get("delivery_address")
        Orders.objects.create(product=product,user=user,delivery_address=delivery_address)
        cart.status="order placed"
        cart.save()
        return redirect("home")














