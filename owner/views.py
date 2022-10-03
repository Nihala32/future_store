from django.shortcuts import render,redirect

# Create your views here.
from django.views.generic import TemplateView,ListView,DetailView
from owner.models import Orders
from owner.forms import OrderUpdateForm

class AdminDashboardView(TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        count=Orders.objects.filter(status="order-placed").count()
        context["count"]=count
        return context


class OrdersListView(ListView):
    model = Orders
    context_object_name = "orders"
    template_name = "admin-listorder.html"

    def get_queryset(self):
        return Orders.objects.filter(status="order-placed")


class OrderDetailView(DetailView):
    model = Orders
    template_name = "order-details.html"
    pk_url_kwarg = "id"
    context_object_name = "order"

    def get_context_data(self, **kwargs):
        context=super().get_context_data()
        form=OrderUpdateForm()
        context["form"]=form

        return context

    def post(self,request,*args,**kwargs):
        order=self.get_object()

        form=OrderUpdateForm(request.POST)
        if form.is_valid():
            order.status=form.cleaned_data.get("status")
            order.expected_date=form.cleaned_data.get("expected_date")
            order.save()

            return redirect("dashboard")



