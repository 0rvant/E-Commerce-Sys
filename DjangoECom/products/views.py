
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView,DetailView
from .models import Product,User,OrderItem,Order,ShippingAddress
from users.models import Customer

# Create your views here.
def index(request):
    return render(request, "users/index.html")


def products(request):  #Products_Store
    pass

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        items =order.orderitem_set.all()
    else:
        items=[]
        order ={'get_cart_total':0,'get_cart_items':0}

    context ={'items':items , 'order':order}
    return render(request, 'products/cart.html',context)



def checkout(request):
    pass

