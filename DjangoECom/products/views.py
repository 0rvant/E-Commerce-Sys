
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import json
import datetime
from django.views.generic import ListView,DetailView
from .models import Product,User,OrderItem,Order,ShippingAddress
from users.models import Customer
from .models import *
from .decorators import *

# Create your views here.
def index(request):
    return render(request, "users/index.html")

def products(request):  #Products_Store
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']

    context = {'products':products , 'order':order ,'cartItems':cartItems}
    return render(request,'products/products.html',context)

@allowed_users(allowed_roles=['customer'])
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


@allowed_users(allowed_roles=['customer'])
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        items =order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items=[]
        order ={'get_cart_total':0,'get_cart_items':0}
        cartItems = order['get_cart_items']

    context ={'items':items , 'order':order,'cartItems':cartItems}
    return render(request, 'products/cart.html',context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created =Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order,product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1 )

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    pass