
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import json
import datetime
from django.views.generic import ListView,DetailView
from .models import Product,User,OrderItem,Order,ShippingAddress
from users.models import Customer
from .models import *
from .decorators import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def index(request):
    return render(request, "users/index.html")

def products(request):  #Products_Store
    products_list = Product.objects.all()
    if request.user.is_authenticated:
        customer=request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items
    else:
        cartItems=0
    # Paginator for products 
    page = request.GET.get('page', 1)
    paginator = Paginator(products_list, 8) #number of products in one page = 8
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products_list = paginator.page(paginator.num_pages)

    #we need to send all Category here to choose one form them in forntend
    context = {'products':products,'cartItems':cartItems}
    return render(request, 'products/products.html', context)

def productDetails(request):  #Products_Store
    productId=request.GET['productId']
    product=Product.objects.get(id=productId)
    if request.user.is_authenticated:
        customer=request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items
    else:
        cartItems=0
    context = {'product':product,'cartItems':cartItems}
    return render(request, 'products/productDetails.html', context)

    #we need to send all Category here to choose one form them in forntend
    context = {'products':products,'cartItems':cartItems}
    return render(request, 'products/products.html', context)
#@allowed_users(allowed_roles=['customer'])
def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        items =order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items=[]
        order ={'get_cart_total':0,'get_cart_items':0}
        cartItems = 0
    context ={'items':items , 'order':order, 'cartItems':cartItems}
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
    elif action == 'delete':
        orderItem.quantity = (orderItem.quantity - orderItem.quantity)
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment submitted..', safe=False)